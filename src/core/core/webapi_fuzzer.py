import jsonpickle
from utils import Utils
from cProfile import run
from cmath import pi
from concurrent.futures import ThreadPoolExecutor
from fuzz_test_result_queue import FuzzTestResultQueue
from threading import Event
from urllib.error import HTTPError
from requests import Request, Response, Session
import requests
from pubsub import pub
import asyncio
from http import cookiejar
from types import MappingProxyType
import shortuuid
from datetime import datetime
from eventstore import EventStore, MsgType
from fuzz_test_result_queue import FuzzTestResultQueue
from models.apicontext import SupportedAuthnType
from models.webapi_fuzzcontext import (ApiFuzzContext, ApiFuzzCaseSet, ApiFuzzDataCase, 
                                       ApiFuzzRequest, ApiFuzzResponse, FuzzTestResult,
                                        FuzzMode, FuzzCaseSetFile, WordlistType)
from graphql_models import ApiFuzzCaseSets_With_RunSummary_ViewModel
import io

from db import (insert_api_fuzzCaseSetRuns,
                update_api_fuzzCaseSetRun_status,
                insert_api_fuzzdatacase, 
                insert_api_fuzzrequest, 
                insert_api_fuzzresponse,
                create_runsummary_per_fuzzcaseset,
                update_casesetrun_summary,
                get_fuzzcaseset_run_statistics,
                insert_api_fuzzrequest_fileupload)
import time
from multiprocessing import Lock
from enum import Enum 
from corporafactory.corpora_context import CorporaContext
from utils import Utils
from requests_toolbelt.multipart.encoder import MultipartEncoder

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
        
    def __del__(self):
        self.eventstore.emitInfo('WebApi Fuzzer shutting down')

            
    def cancel_fuzzing(self, errorMsg = ''):
        try:
            
            self.fuzzingStatus = FuzzingStatus.Stop
            
            self.multithreadEventSet.set()
            
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.totaRunsPerCaseSet = 0
            
            update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId, status='cancelled', message=errorMsg)
            
        except Exception as e:
            self.eventstore.emitErr(e)
    
    async def fuzz_once(self):
        try:
            
            self.corporaContext.build_context(self.apifuzzcontext.fuzzcaseSets)
            
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
                
                create_runsummary_per_fuzzcaseset(Id = caseSetRunSummaryId,
                                          fuzzCaseSetId=  fcs.Id,
                                          fuzzCaseSetRunId = self.fuzzCaseSetRunId,
                                          fuzzcontextId = self.apifuzzcontext.Id,
                                          totalRunsToComplete = self.totaRunsPerCaseSet)
                
                for _ in range(self.apifuzzcontext.fuzzcaseToExec):
                    
                    runNumber = runNumber + 1
                    
                    self.executor.submit(self.fuzz_each_fuzzcaseset, caseSetRunSummaryId, fcs, self.multithreadEventSet, runNumber)
                    
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.begin_fuzzing')
        
    async def fuzz(self):
        
        if self.apifuzzcontext == None or len(self.apifuzzcontext.fuzzcaseSets) == 0:
            self.eventstore.emitErr(f'WebApiFuzzer detected empty ApiFuzzContext: {self.apifuzzcontext}')
            return
        
        await self.begin_fuzzing()
        
    async def begin_fuzzing(self):
          
        try:
            
            self.corporaContext.build_context(self.apifuzzcontext.fuzzcaseSets)
            
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
                
                create_runsummary_per_fuzzcaseset(Id = caseSetRunSummaryId,
                                          fuzzCaseSetId=  fcs.Id,
                                          fuzzCaseSetRunId = self.fuzzCaseSetRunId,
                                          fuzzcontextId = self.apifuzzcontext.Id,
                                          totalRunsToComplete = self.totaRunsPerCaseSet)
                
                for _ in range(self.apifuzzcontext.fuzzcaseToExec):
                    
                    runNumber = runNumber + 1
                    
                    self.executor.submit(self.fuzz_each_fuzzcaseset, caseSetRunSummaryId, fcs, self.multithreadEventSet, runNumber)
                    
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.begin_fuzzing')
            
    def fuzz_each_fuzzcaseset(self, caseSetRunSummaryId, fcs: ApiFuzzCaseSet, multithreadEventSet: Event, runNumber: int):
        
        try:
            if multithreadEventSet.is_set():
                return
            
            fuzzDataCase, file = self.http_call(fcs)
            
            summaryViewModel = self.enqueue_fuzz_result_for_persistent(caseSetRunSummaryId, fuzzDataCase, file)
            
            self.save_uploaded_file(file=file,fuzzRequestId=fuzzDataCase.request.Id, fuzzDataCaseId=fuzzDataCase.Id )
            
            # update run status
            self.fuzzcaseset_done(runNumber)
                
            if summaryViewModel is not None:
                self.eventstore.feedback_client('fuzz.update.casesetrunsummary', summaryViewModel)
            
        except Exception as e:
            errMsg = Utils.errAsText(e)
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzz_each_fuzzcaseset')
            self.cancel_fuzzing(errorMsg=errMsg)
            
    def http_call(self, fcs: ApiFuzzCaseSet) -> tuple([ApiFuzzDataCase, dict]):
        
        resp = None
        
        try:
            
            fuzzDataCase = self.create_fuzzdatacase(fuzzcaseSetId=fcs.Id,
                                                    fuzzcontextId=self.apifuzzcontext.Id)
            
            # url already includes hostname, port, path and qs
            # files = list[tuple(wordlistType, filename, content)]
            ok, err, hostname, port, hostnamePort, url, path, querystring, body, headers, file = self.dataprep_fuzzcaseset( self.apifuzzcontext, fcs)
            
            # problem exist in fuzz data preparation, cannot continue.
            if not ok:
                self.eventstore.emitErr(Exception('Error at data prep when fuzzing: {err}'))
                return
            
            contentType = self.determine_and_set_content_type(headers)
            
            reqBody = ''
            reqBody = self.try_decode_body(body)

            try:
                req = None                
                
                if file != None and reqBody != '':
                    if contentType == 'application/x-www-form-urlencoded':
                        
                        # need to covert 'aaa=1&bbb=2&ccc=yeah' to dict
                        # supporting the above data format is purely to support syntax from rest-client 
                        
                        wwwformurlencodedDict = self.create_dict_for_wwwformurlencoded(reqBody)
                        
                        req = Request(fcs.verb, url, headers=headers, data=wwwformurlencodedDict)
                      
                    # elif contentType == 'application/json':
                    #     req = Request(fcs.verb, url, headers=headers, json=reqBody)
                        
                    # elif contentType == 'application/xml':
                    #     req = Request(fcs.verb, url, headers=headers, data=reqBody)
                    else:
                        req = Request(fcs.verb, url, headers=headers, data=reqBody)

                elif file != None:
                    
                    # support single file only.
                    # fuzzie's goal is to upload file content as the "whole" POST body.
                    # with multiple files being uploaded, multipart-form headers Content-Disposition will be included as file content.
                    # which fuzzie tries to avoid altering original file content
                    if Utils.isNoneEmpty(file.content):
                        self.eventstore.emitErr(Exception(f'fuzz data wordlist-type {file.wordlist_type} content is empty'))
                    else:
                        content = file.content
                
                    req = Request(fcs.verb, url, headers=headers, data=content)
                else:
                    req = Request(fcs.verb, url, headers=headers)
                
                
                headers['User-Agent'] = 'fuzzie'

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
                        contentLength=reqContentLength)
                
                httpSession = Session()
                resp = httpSession.send(prepReq, timeout=self.httpTimeoutInSec, allow_redirects=False, verify=False)
            
            except Exception as e:
                err =  Utils.errAsText(e)
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
            
            err = Utils.errAsText(e)
            
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
                err =  Utils.errAsText(e)
                fr.statusCode = 400 if err.find('timed out') == -1 else 508 #400 client error
                fr.reasonPharse = f'{err}'
            
            fuzzDataCase.response = fr
            
        return fuzzDataCase, file

             
    def fuzzcaseset_done(self, runNumber):
        
        try:
                
            # check if last task, to end fuzzing
            if runNumber >= self.totalRunsForAllCaseSets:
                
                update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId)
                
                self.fuzzingStatus = FuzzingStatus.Stop
                
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzzcaseset_done')
    
    def save_uploaded_file(self, file: FuzzCaseSetFile, fuzzDataCaseId, fuzzRequestId):
        
        try:
            if file != None:
                wordlist_type = file.wordlist_type
                fileName = file.filename
                content = file.content
                insert_api_fuzzrequest_fileupload(
                    Id=shortuuid.uuid(),
                    wordlist_type=wordlist_type,
                    fileName=fileName,
                    fileContent= content,
                    fuzzcontextId= self.apifuzzcontext.Id,
                    fuzzDataCaseId=fuzzDataCaseId,
                    fuzzRequestId=fuzzRequestId
                )
                    

        except Exception as e:
            self.eventstore.emitErr(e)
        
    def enqueue_fuzz_result_for_persistent(self, caseSetRunSummaryId, fdc: ApiFuzzDataCase, file) -> ApiFuzzCaseSets_With_RunSummary_ViewModel:
    
        try:
            
            fuzztestResult = FuzzTestResult(fdc=fdc, 
                                            fuzzcontextId=fdc.fuzzcontextId, 
                                            fuzzCaseSetId=fdc.fuzzCaseSetId,
                                            fuzzCaseSetRunId=self.fuzzCaseSetRunId, 
                                            caseSetRunSummaryId=caseSetRunSummaryId, 
                                            file=file,
                                            httpCode=int(fdc.response.statusCode), 
                                            completedDataCaseRuns=1 )
            
            FuzzTestResultQueue.enqueue(fuzztestResult)
            
            # background task result saver is upadting run-statistics
            runSummaryStatistics = get_fuzzcaseset_run_statistics(fuzzcontextId=fdc.fuzzcontextId,
                                           caseSetRunSummaryId=caseSetRunSummaryId,
                                           fuzzCaseSetId=fdc.fuzzCaseSetId,
                                           fuzzCaseSetRunId=self.fuzzCaseSetRunId)
            
            return runSummaryStatistics
            
        except Exception as e:
            errMsg = Utils.errAsText(e)
            self.eventstore.emitErr(f'Error when saving fuzzdatacase, fuzzrequest and fuzzresponse: {errMsg}', data='WebApiFuzzer.enqueue_fuzz_result_for_persistent')
                
            
    def create_fuzzrequest(self, fuzzDataCaseId, fuzzcontextId, hostname, port, hostnamePort, verb, path, qs, url, headers, body, contentLength=0, invalidRequestError=''):
        
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
            file = None        #for openapi3 single file only
            
            okpath, errpath, resolvedPathDT = self.corporaContext.resolve_fuzzdata(pathDT) #self.inject_fuzzdata_in_datatemplate(pathDT)
            if not okpath:
                return [False, errpath, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            okqs, errqs, resolvedQSDT = self.corporaContext.resolve_fuzzdata(querystringDT) #self.inject_fuzzdata_in_datatemplate(querystringDT)
            if not okqs:
                return [False, errqs, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            okbody, errbody, resolvedBodyDT = self.corporaContext.resolve_fuzzdata(bodyDT) #self.inject_fuzzdata_in_datatemplate(bodyDT)
            if not okbody:
                return [False, errbody, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            # header - reason for looping over each header data template and getting fuzz data is to 
            # prevent json.dump throwing error from Json reserved characters 
            headerDict = {}
            headerDTObj = Utils.try_parse_json_to_object(headerDT)
            if Utils.dict_has_items(headerDTObj):
                
                for hk in headerDTObj.keys():
                    dt = headerDTObj[hk]
                    
                    ok, err, resolvedVal = self.corporaContext.resolve_fuzzdata(dt) #self.inject_fuzzdata_in_datatemplate(dataTemplate)
                    
                    if not ok:
                        self.eventstore.emitErr(err, 'webapi_fuzzer.dataprep_fuzzcaseset')
                        continue
                    
                    headerDict[hk] = resolvedVal
                
                    
            # handle file upload with "proper" encoding,
            # without encoding requests will throw error as requests uses utf-8 by default
            if fcs.file != '':
                
                ok = True
                err = ''
                fileContent = ''
                fileWordlistType = fcs.file
                filename = self.corporaContext.cp.fileNameCorpora.next_corpora(fileType=fileWordlistType)
                
                if FuzzCaseSetFile.is_myfile(fcs.file):
                    ok, err, fileContent = self.corporaContext.resolve_fuzzdata(fcs.fileDataTemplate)
                    
                    decoded = self.try_decode_file_content(fileContent)
                    
                    file = FuzzCaseSetFile(wordlist_type=WordlistType.myfile, filename=filename, content=decoded)
                # image, file, pdf
                else:
                    ok, err, fileContent = self.corporaContext.resolve_file(fcs.file)
                    
                    #decoded = self.try_decode_file_content(fileContent)
                    
                    file = FuzzCaseSetFile(wordlist_type=fcs.file, filename=filename, content=fileContent)
                    
                    
            url = f'{hostnamePort}{resolvedPathDT}{resolvedQSDT}'
            
            authnHeader= self.determine_authn_scheme(fc)
                    
            headers = {**authnHeader, **headerDict}     #merge 2 dicts
            
            return [True, '', hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers, file]
        
        except Exception as e:
            errText =  Utils.errAsText(e)
            self.eventstore.emitErr(f'Error {errText}', data='WebApiFuzzer.dataprep_fuzzcaseset')
            return [False, errText, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers, file]
    
    
    def try_decode_file_content(self, content):
        decoded = content
        
        latinOK, latinDecoded = Utils.try_decode_latin1(content)
        if latinOK:
            decoded = latinDecoded
        else:
            utf8OK, utf8Decoded = Utils.try_decode_utf8(content)
            if utf8OK:
                decoded = utf8Decoded
                
        return decoded
    
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
    
    def create_dict_for_wwwformurlencoded(self, wwwformurl: str)-> dict:
        
        if wwwformurl == '':
            return {}
        
        result = {}
        
        keyval = wwwformurl.split('&')
        
        for kv in keyval:
            
            key = kv[0]
            val = kv[1]
            
            if key != '' and val != '':
                result[key] = val
                
        return result
    
    