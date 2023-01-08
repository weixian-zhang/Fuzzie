import jsonpickle
from utils import Utils
from cProfile import run
from cmath import pi
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from urllib.error import HTTPError
from requests import Request, Response, Session
import requests
from pubsub import pub
import json
from http import cookiejar
from types import MappingProxyType
import shortuuid
from datetime import datetime
from eventstore import EventStore, MsgType
from models.apicontext import SupportedAuthnType
from models.webapi_fuzzcontext import (ApiFuzzContext, ApiFuzzCaseSet, ApiFuzzDataCase, 
                                       ApiFuzzRequest, ApiFuzzResponse, 
                                        FuzzMode)
from graphql_models import ApiFuzzCaseSets_With_RunSummary_ViewModel

from db import (insert_api_fuzzCaseSetRuns,
                update_api_fuzzCaseSetRun_status,
                insert_api_fuzzdatacase, 
                insert_api_fuzzrequest, 
                insert_api_fuzzresponse,
                create_casesetrun_summary,
                update_casesetrun_summary,
                insert_api_fuzzrequest_fileupload)
import time
from multiprocessing import Lock
from enum import Enum 
from corporafactory.corpora_context import CorporaContext
from utils import Utils

class FuzzingStatus(Enum):
    Fuzzing = 1
    Stop = 2

class WebApiFuzzer:
    
    def __init__(self, apifuzzcontext: ApiFuzzContext) -> None:
                    # basicUsername = '',
                    # basicPassword = '',
                    # bearerTokenHeader = 'Authorization',
                    # bearerToken = '',
                    # apikeyHeader = '',
                    # apikey = '') -> None:
        
        # supports remember Set-Cookie from response
        #cookie example
        # contain in single header = cookie1=value1;cookie2=value2
        # Set-Cookie: chocolate=chips; expires=Sun, 15-Nov-2009 18:47:08 GMT; path=/; domain=thaorius.net; secure; httponly
        # Set-Cookie: milk=shape
        self.cookiejar = {}
        
        self.fuzzingStatus : FuzzingStatus = FuzzingStatus.Fuzzing
        
        # security creds
        self.basicUsername = apifuzzcontext.basicUsername,
        self.basicPassword = apifuzzcontext.basicPassword,
        self.bearerTokenHeader = apifuzzcontext.bearerTokenHeader,
        self.bearerToken = apifuzzcontext.bearerToken,
        self.apikeyHeader = apifuzzcontext.apikeyHeader,
        self.apikey = apifuzzcontext.apikey
        
        self.httpTimeoutInSec = 4
        self.fuzzCaseSetRunId = shortuuid.uuid()
        
        self.totalRunsForAllCaseSets = 0
        self.totaRunsPerCaseSet = 0
        
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        self.multithreadEventSet = Event()
        
        # self.processLock = Lock()
        # self.dbLock = Lock()
        
        self.eventstore = EventStore()
        self.apifuzzcontext = apifuzzcontext
        
        self.corporaContext = CorporaContext()
        
        #subscribe cancel-fuzzing event
        #pub.subscribe( listener=self.pubsub_command_receiver, topicName= self.eventstore.CancelFuzzWSTopic)

            
    def cancel_fuzzing(self, errorMsg = ''):
        try:
            
            self.multithreadEventSet.set()
            
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.totaRunsPerCaseSet = 0
            
            update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId, status='cancelled', message=errorMsg)
            
            self.fuzzingStatus = FuzzingStatus.Stop
     
        except Exception as e:
            self.eventstore.emitErr(e)
        
        
    def fuzz(self):
        
        if self.apifuzzcontext == None or len(self.apifuzzcontext.fuzzcaseSets) == 0:
            self.eventstore.emitErr(f'WebApiFuzzer detected empty ApiFuzzContext: {self.apifuzzcontext}')
            return
        
        self.begin_fuzzing()
        
    def begin_fuzzing(self):
          
        try:
            
            self.build_corpora_context(self.apifuzzcontext.fuzzcaseSets)
            
            insert_api_fuzzCaseSetRuns(self.fuzzCaseSetRunId, self.apifuzzcontext.Id)
                        
            self.fuzzingStatus = FuzzingStatus.Fuzzing
            
            fcsLen = len(self.apifuzzcontext.fuzzcaseSets)
            
            if fcsLen == 0:
                self.eventstore.emitErr(f"no fuzz case detected for fuzz-context {self.apifuzzcontext.name}, fuzzing stopped")
                return
            
            self.totaRunsPerCaseSet = self.apifuzzcontext.fuzzcaseToExec
            self.totalRunsForAllCaseSets = fcsLen * self.totaRunsPerCaseSet
            
            runNumber = 0
            for fcs in self.apifuzzcontext.fuzzcaseSets:
                
                caseSetRunSummaryId = shortuuid.uuid()
                
                create_casesetrun_summary(Id = caseSetRunSummaryId,
                                          fuzzCaseSetId=  fcs.Id,
                                          fuzzCaseSetRunId = self.fuzzCaseSetRunId,
                                          fuzzcontextId = self.apifuzzcontext.Id,
                                          totalRunsToComplete = self.totaRunsPerCaseSet)
                
                for _ in range(self.apifuzzcontext.fuzzcaseToExec):
                    
                    runNumber = runNumber + 1
                    
                    self.executor.submit(self.fuzz_each_fuzzcaseset, caseSetRunSummaryId, fcs, self.multithreadEventSet, runNumber )
                    
                    
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.begin_fuzzing')
            
    def build_corpora_context(self, fcss: list[ApiFuzzCaseSet]):
        
        for fcs in fcss:
            
            if self.isDataTemplateEmpty(fcs.pathDataTemplate) == False:
                self.corporaContext.build(fcs.pathDataTemplate)
                
            if self.isDataTemplateEmpty(fcs.querystringDataTemplate) == False:
                self.corporaContext.build(fcs.querystringDataTemplate)
                
            if self.isDataTemplateEmpty(fcs.headerDataTemplate) == False:
                self.corporaContext.build(fcs.headerDataTemplate)
            
            if self.isDataTemplateEmpty(fcs.bodyDataTemplate) == False:
                self.corporaContext.build(fcs.bodyDataTemplate)
                
            self.corporaContext.build_files(fcs.file)
        
    def fuzz_each_fuzzcaseset(self, caseSetRunSummaryId, fcs: ApiFuzzCaseSet, multithreadEventSet: Event, runNumber: int):
        
        try:
            if multithreadEventSet.is_set():
                return
            
            fuzzDataCase, files = self.http_call_api(fcs)
            
            summaryViewModel = self.save_fuzzDataCase(caseSetRunSummaryId, fuzzDataCase)
            
            self.save_uploaded_files(files=files,fuzzRequestId=fuzzDataCase.request.Id, fuzzDataCaseId=fuzzDataCase.Id )
            
            # update run status
            self.fuzzcaseset_done(runNumber)
                
            if summaryViewModel is not None:
                self.eventstore.feedback_client('fuzz.update.casesetrunsummary', summaryViewModel)
            
            #reduce payload size, the following properties will be retrieved separately by webview "onClick"
            # fuzzDataCase.request.body = ''
            # fuzzDataCase.request.requestMessage = ''
            # fuzzDataCase.response.responseDisplayText = ''
            # self.eventstore.feedback_client('fuzz.update.fuzzdatacase', fuzzDataCase)
            
        except Exception as e:
            errMsg = Utils.errAsText(e)
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzz_each_fuzzcaseset')
            self.cancel_fuzzing(errorMsg=errMsg)
            
    def http_call_api(self, fcs: ApiFuzzCaseSet) -> tuple([ApiFuzzDataCase, dict]):
        
        resp = None
        
        try:
            
            fuzzDataCase = self.create_fuzzdatacase(fuzzcaseSetId=fcs.Id,
                                                    fuzzcontextId=self.apifuzzcontext.Id)
            
            # url already includes hostname, port, path and qs
            ok, err, hostname, port, hostnamePort, url, path, querystring, body, headers, files = self.dataprep_fuzzcaseset( self.apifuzzcontext, fcs)
            
            # problem exist in fuzz data preparation, cannot continue.
            if not ok:
                self.eventstore.emitErr(Exception('Error at data prep when fuzzing: {err}'))
                return
            
            contentType = self.determine_and_set_content_type(headers)
            
            reqBody = ''
            reqBody = self.try_decode_body(body)

            try:
                req = None
                
                if contentType == 'application/x-www-form-urlencoded':
                    req = Request(fcs.verb, url, headers=headers, data=reqBody)
                    
                elif contentType == 'application/json':
                    req = Request(fcs.verb, url, headers=headers, json=reqBody)
                    
                elif contentType == 'application/xml':
                    req = Request(fcs.verb, url, headers=headers, data=reqBody)
                    
                elif len(files) > 0:   
                    req = Request(fcs.verb, url, headers=headers, json=reqBody, files=files)
                    
                else:
                    if fcs.verb == 'GET':
                        req = Request(fcs.verb, url, headers=headers)
                    else:
                        req = Request(fcs.verb, url, headers=headers, json=reqBody)
                
                
                prepReq = req.prepare()
                
                reqContentLength =  0
                if 'Content-Length' in prepReq.headers:
                    reqContentLength = prepReq.headers['Content-Length']
                
                fuzzDataCase.request = self.create_fuzzrequest(
                        fuzzDataCaseId=fuzzDataCase.Id,
                        fuzzcontextId=self.apifuzzcontext.Id,
                        hostname=hostname, 
                        port=port,
                        hostnamePort=hostnamePort,
                        url=url,
                        path=path,
                        qs=querystring,
                        verb=fcs.verb,
                        headers=headers,
                        body=reqBody,
                        contentLength=reqContentLength,
                        files=files)
                
                httpSession = Session()
                resp = httpSession.send(prepReq, timeout=self.httpTimeoutInSec, allow_redirects=False, verify=False)
            
            except Exception as e:
                err =  Utils.errAsText(e.args)
                fuzzDataCase.request = self.create_fuzzrequest(
                                        fuzzDataCaseId=fuzzDataCase.Id,
                                        fuzzcontextId=self.apifuzzcontext.Id,
                                        hostname=hostname, 
                                        port=port,
                                        hostnamePort=hostnamePort,
                                        url=url,
                                        path=path,
                                        qs=querystring,
                                        verb=fcs.verb,
                                        headers=headers,
                                        body=reqBody,
                                        contentLength=0,
                                        invalidRequestError=err)
                
                self.cancel_fuzzing(errorMsg=Utils.errAsText(e))
                
                return fuzzDataCase, {}
            
            
            try:
                fuzzResp = self.create_fuzz_response(self.apifuzzcontext.Id, fuzzDataCase.Id, resp)
            
                fuzzDataCase.response = fuzzResp
                
                self.save_resp_cookie_if_exists(hostnamePort, fuzzResp.setcookieHeader) 
                
            except Exception as e:
                self.eventstore.emitErr(e)
                self.cancel_fuzzing(errorMsg=Utils.errAsText(e))
            
        except HTTPError as e:
            
            err = Utils.jsone(e.args)
            
            fr = ApiFuzzResponse()
            fr.Id = shortuuid.uuid()
            fr.datetime = datetime.now()
            fr.fuzzcontextId = self.apifuzzcontext.Id
            fr.fuzzDataCaseId = fuzzDataCase.Id
            fr.statusCode = e.code
            fr.reasonPharse = err
            fuzzDataCase.response = fr
            
        except Exception as e:
            
            fr = ApiFuzzResponse()
            fr.Id = shortuuid.uuid()
            fr.datetime = datetime.now()
            fr.fuzzcontextId = self.apifuzzcontext.Id
            fr.fuzzDataCaseId = fuzzDataCase.Id
            fr.responseDisplayText = ''
                
            if resp != None:
                fr.statusCode = resp.status_code
                fr.reasonPharse = resp.reason
                fr.body = resp.text
            else:  
                err =  Utils.jsone(e.args)
                fr.statusCode = 400 if err.find('timed out') == -1 else 508 #400 client error
                fr.reasonPharse = f'{err}'
            
            fuzzDataCase.response = fr
            
        return fuzzDataCase, files

             
    def fuzzcaseset_done(self, runNumber):
        
        try:
                
            # check if last task, to end fuzzing
            if runNumber >= self.totalRunsForAllCaseSets:
                
                update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId)
                
                self.fuzzingStatus = FuzzingStatus.Stop
                
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzzcaseset_done')
    
    def save_uploaded_files(self, files, fuzzDataCaseId, fuzzRequestId):
        
        try:
            if len(files) > 0:
                for ftuple in files:
                    fileName, content = ftuple
                    insert_api_fuzzrequest_fileupload(
                        Id=shortuuid.uuid(),
                        fileName=fileName,
                        fileContent= content,
                        fuzzcontextId= self.apifuzzcontext.Id,
                        fuzzDataCaseId=fuzzDataCaseId,
                        fuzzRequestId=fuzzRequestId
                    )

        except Exception as e:
            self.eventstore.emitErr(e)
        
    def save_fuzzDataCase(self, caseSetRunSummaryId, fdc: ApiFuzzDataCase) -> ApiFuzzCaseSets_With_RunSummary_ViewModel:
    
        try:
            
            insert_api_fuzzdatacase(self.fuzzCaseSetRunId, fdc)
            
            insert_api_fuzzrequest(fdc.request)
            
            if fdc.response is not None and fdc.response != {}:
                insert_api_fuzzresponse(fdc.response)
                
                # update run summary
                summaryViewModel = update_casesetrun_summary(
                                                             fuzzcontextId=fdc.fuzzcontextId, 
                                                             fuzzCaseSetRunId=self.fuzzCaseSetRunId, 
                                                             fuzzCaseSetId=fdc.fuzzCaseSetId, 
                                                             Id=caseSetRunSummaryId,
                                                            httpCode=int(fdc.response.statusCode),
                                                            completedDataCaseRuns=1
                                                            )
                
                return summaryViewModel
            
            return None
            
        except Exception as e:
            ej = Utils.jsone(e)
            self.eventstore.emitErr(f'Error when saving fuzzdatacase, fuzzrequest and fuzzresponse: {ej}', data='WebApiFuzzer.save_fuzzDataCase')
                
            
    def create_fuzzrequest(self, fuzzDataCaseId, fuzzcontextId, hostname, port, hostnamePort, verb, path, qs, url, headers, body, contentLength=0, invalidRequestError='', files=[]):
        
        try:
            fr = ApiFuzzRequest()
        
            fr.Id = shortuuid.uuid()
            fr.datetime = datetime.now()
            fr.fuzzDataCaseId = fuzzDataCaseId
            fr.fuzzcontextId = fuzzcontextId
            fr.hostname = hostname
            fr.port = port
            fr.hostnamePort = hostnamePort
            fr.verb = verb
            fr.path = path
            fr.querystring = qs
            fr.url = url
            fr.headers = Utils.jsone(headers)
            fr.body = Utils.b64e(body)
            fr.contentLength = contentLength
            fr.invalidRequestError = invalidRequestError
            
            headerMultilineText = ''
            
            if type(headers) is dict and len(headers) > 0:
                for x in headers.keys():
                    headerMultilineText = headerMultilineText + f'{x}:{headers[x]}\n'
                
            rm = f'{fr.verb} {fr.url}' \
                                 '\n' \
                                 '\n' \
                                f'{headerMultilineText}' \
                                 '\n' \
                                f'{body if body != "{}" else ""}'
                                
            fr.requestMessage = Utils.b64e(rm)
            
            return fr
        
        except Exception as e:
            ej = Utils.jsone(e)
            self.eventstore.emitErr(f'Error when saving fuzzdatacase, fuzzrequest and fuzzresponse: {ej}', data='WebApiFuzzer.create_fuzzrequest')
        
            
    def create_fuzz_response(self, fuzzcontextId, fuzzDataCaseId, resp: Response) -> ApiFuzzResponse:
        
        if resp is None:
            return None
        
        try:
            fuzzResp = ApiFuzzResponse()
        
            fuzzResp.Id = shortuuid.uuid()
            fuzzResp.datetime = datetime.now()
            fuzzResp.fuzzDataCaseId = fuzzDataCaseId
            fuzzResp.fuzzcontextId = fuzzcontextId 
            
            fuzzResp.statusCode = resp.status_code
            fuzzResp.reasonPharse = resp.reason
            fuzzResp.body = Utils.b64e(resp.text)
            
            headers = {}
            headersMultilineText = ''
            for k in resp.headers.keys():
                headers[k] = resp.headers[k]
                headersMultilineText = headersMultilineText + f'{k}: {resp.headers[k]}\n'
                
            fuzzResp.headersJson = Utils.jsone(headers)
                
            fuzzResp.setcookieHeader = self.try_get_setcookie_value(headers)
            
            fuzzResp.contentLength = resp.headers['Content-Length']
            
            respDT = f'{fuzzResp.statusCode} {fuzzResp.reasonPharse} ' \
                                        '\n' \
                                        f'{headersMultilineText}' \
                                        '\n' \
                                        f'Content-Length: {fuzzResp.contentLength}' \
                                        '\n' \
                                        '\n' \
                                        f'{resp.text}'
            
            fuzzResp.responseDisplayText =  Utils.b64e(respDT)                   
            
            return fuzzResp
        except Exception as e:
            self.eventstore.emitErr(e)
        
        
    def determine_and_set_content_type(self, headers: dict):
        contentType = ''
        if headers is None or 'Content-Type' not in headers:
            return contentType
        else:
            contentType = headers['Content-Type']
        
        return contentType
                
    def try_get_setcookie_value(self, respHeadersDict: dict):
        result = ''
        setCookieHeader = 'Set-Cookie'
        if setCookieHeader in respHeadersDict.keys():
            result = respHeadersDict[setCookieHeader]
        return result
                     
    def save_resp_cookie_if_exists(self, hostname, cookie):
        if cookie == '':
            return
        
        if not hostname in self.cookiejar.keys():
            self.cookiejar[hostname] = cookie
        
    def dataprep_fuzzcaseset(self, fc: ApiFuzzContext, fcs: ApiFuzzCaseSet):            
            
        try:
            
            hostname = fcs.hostname
            port = fcs.port
            hostnamePort = f'{hostname}:{port}' #fc.get_hostname_port()
            pathDT = fcs.get_path_datatemplate()
            querystringDT = fcs.querystringDataTemplate
            bodyDT= fcs.bodyDataTemplate
            headerDT = fcs.headerDataTemplate
            files = []          #for openapi3 single file only
            
            okpath, errpath, resolvedPathDT = self.corporaContext.resolve_expr(pathDT) #self.inject_fuzzdata_in_datatemplate(pathDT)
            if not okpath:
                return [False, errpath, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            okqs, errqs, resolvedQSDT = self.corporaContext.resolve_expr(querystringDT) #self.inject_fuzzdata_in_datatemplate(querystringDT)
            if not okqs:
                return [False, errqs, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            okbody, errbody, resolvedBodyDT = self.corporaContext.resolve_expr(bodyDT) #self.inject_fuzzdata_in_datatemplate(bodyDT)
            if not okbody:
                return [False, errbody, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            # header - reason for looping over each header data template and getting fuzz data is to 
            # prevent json.dump throwing error from Json reserved characters 
            headerDict = {}
            headerDTObj = Utils.try_parse_json_to_object(headerDT)
            if Utils.dict_has_items(headerDTObj):
                
                for hk in headerDTObj.keys():
                    dt = headerDTObj[hk]
                    
                    ok, err, resolvedVal = self.corporaContext.resolve_expr(dt) #self.inject_fuzzdata_in_datatemplate(dataTemplate)
                    
                    if not ok:
                        self.eventstore.emitErr(err, 'webapi_fuzzer.dataprep_fuzzcaseset')
                        continue
                    
                    headerDict[hk] = resolvedVal
                
                    
            # handle file upload with "proper" encoding, without encoding requests will throw error as requests uses utf-8 by default
            if len(fcs.file) > 0:
                for fileType in fcs.file:
                    ok, err, fileContent = self.corporaContext.resolve_file(fileType)
                    if ok:
                        filename = self.corporaContext.cp.fileNameCorpora.next_corpora()
                        
                        if fileType == 'file':
                            files.append((filename, fileContent.decode('latin1')))
                            
                        elif fileType == 'image':
                            files.append((filename, fileContent.decode('latin1')))
                            
                        elif fileType == 'pdf':
                            files.append((filename, fileContent.decode('latin1')))
                            
                        else:
                            files.append((filename, fileContent.decode('latin1')))
            
            url = f'{hostnamePort}{resolvedPathDT}{resolvedQSDT}'
            
            authnHeader= self.determine_authn_scheme(fc)
                    
            headers = {**authnHeader, **headerDict}     #merge 2 dicts
            
            return [True, '', hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers, files]
        
        except Exception as e:
            errText =  Utils.errAsText(e)
            self.eventstore.emitErr(f'Error {errText}', data='WebApiFuzzer.dataprep_fuzzcaseset')
            return [False, errText, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers, files]
    
    # returns dict representing header
    def determine_authn_scheme(self, fc: ApiFuzzContext) -> dict:
        securityHeaders = {}
        
        if fc.authnType == SupportedAuthnType.Anonymous.name:
            return {}
        
        if fc.authnType == SupportedAuthnType.Basic.name:
            return {
                    'Authorization': f'Basic {self.apifuzzcontext.basicUsername}:{self.apifuzzcontext.basicPassword}'
                   }
        
        elif fc.authnType == SupportedAuthnType.Bearer.name:
            return {
                    f'{self.apifuzzcontext.bearerTokenHeader}': f'{self.apifuzzcontext.bearerToken}'
                   }

        elif fc.authnType == SupportedAuthnType.ApiKey.name:
            
            return {
                    f'{self.apifuzzcontext.apikeyHeader}': f'{self.apifuzzcontext.apikey}'
                   }
            
        return {}
    
    def try_decode_body(self, body):
        try:
            if body == '':
                return body
            
            dbody = body.decode('utf-8')
            return dbody
        except Exception as e:
            return body

    def create_fuzzdatacase(self, fuzzcaseSetId, fuzzcontextId):
        
        fdc = ApiFuzzDataCase()
        fdc.Id = shortuuid.uuid()
        fdc.fuzzCaseSetId = fuzzcaseSetId
        fdc.fuzzcontextId = fuzzcontextId
        return fdc
    
    def isDataTemplateEmpty(self, template):
        if template == '' or template == '{}':
            return True
        
        return False
    
    