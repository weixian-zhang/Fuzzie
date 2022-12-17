import jsonpickle
from utils import Utils
from cProfile import run
from cmath import pi
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
from requests import Request, Response, Session
import requests
from pubsub import pub
from http import cookiejar
from types import MappingProxyType
import shortuuid
from datetime import datetime
from eventstore import EventStore, MsgType
import json
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
                update_casesetrun_summary)

from multiprocessing import Lock

from corporafactory.corpora_context import CorporaContext        

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
        
        # security creds
        self.basicUsername = apifuzzcontext.basicUsername,
        self.basicPassword = apifuzzcontext.basicPassword,
        self.bearerTokenHeader = apifuzzcontext.bearerTokenHeader,
        self.bearerToken = apifuzzcontext.bearerToken,
        self.apikeyHeader = apifuzzcontext.apikeyHeader,
        self.apikey = apifuzzcontext.apikey
        
        self.httpTimeoutInSec = 2
        self.fuzzCancel = False
        self.fuzzCaseSetRunId = shortuuid.uuid()
        self.totalFuzzRuns = 0
        self.currentFuzzRuns = 0
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        self.processLock = Lock()
        self.dbLock = Lock()
        
        self.eventstore = EventStore()
        self.apifuzzcontext = apifuzzcontext
        
        self.corporaContext = CorporaContext()
        
        # self.passwordGenerator = HackedPasswordGenerator()
        # self.usernameGenerator = HackedUsernameGenerator()
        # self.fileGenerator = NaughtyFileGenerator() 
        # self.datetimeGenerator = NaughtyDateTimeGenerator() 
        # self.digitGenerator = NaughtyDigitGenerator() 
        # self.stringGenerator = NaughtyStringGenerator() 
        # self.boolGenerator = NaughtyBoolGenerator() 
        # self.usernameGenerator = HackedUsernameGenerator()
        # self.CharGenerator = ObedientCharGenerator()
        
        pub.subscribe( listener=self.pubsub_command_receiver, topicName= self.eventstore.CancelFuzzingEventTopic)


    def pubsub_command_receiver(self, command):
        
        if command == 'cancel_fuzzing':
            self.cancel_fuzzing()
            
    def cancel_fuzzing(self):
        try:
            
            self.fuzzCancel = True
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.totalFuzzRuns = 0
            self.currentFuzzRuns = 0
            
            self.dbLock.acquire()
            update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId, status='cancelled')
            self.dbLock.release()
            
        except Exception as e:
            self.eventstore.emitErr(e)
        
        
    def fuzz(self):
        
        if self.apifuzzcontext == None or len(self.apifuzzcontext.fuzzcaseSets) == 0:
            self.eventstore.emitErr(f'WebApiFuzzer detected empty ApiFuzzContext: {self.apifuzzcontext}')
            return
        
        self.eventstore.emitInfo(f'start fuzzing {self.apifuzzcontext.name}')
        
        self.begin_fuzzing()
        
    def begin_fuzzing(self):
          
        try:
            
            self.build_corpora_context(self.apifuzzcontext.fuzzcaseSets)
            
            # create a fuzzcaserun record
            self.dbLock.acquire()
            insert_api_fuzzCaseSetRuns(self.fuzzCaseSetRunId, self.apifuzzcontext.Id)
            self.dbLock.release()
            
            
            # self.totalFuzzRuns = 1 # uncomment for testing only
            # self.apifuzzcontext.fuzzcaseToExec = 1 # uncomment for testing only
            
            fcsLen = len(self.apifuzzcontext.fuzzcaseSets)
            
            if fcsLen == 0:
                self.eventstore.emitErr(f"no fuzz case detected for fuzz-context {self.apifuzzcontext.name}, fuzzing stopped")
                return
            
            self.totalFuzzRuns = fcsLen * self.apifuzzcontext.fuzzcaseToExec
            
            # notify fuzzing started
            # pub.sendMessage(self.eventstore.FuzzingStartEventTopic, command='fuzzing_start', msgData=self.apifuzzcontext.Id)
            self.eventstore.feedback_client('fuzz.start', {'fuzzCaseSetRunId': self.fuzzCaseSetRunId, 'fuzzcontextId': self.apifuzzcontext.Id})
            
            for fcs in self.apifuzzcontext.fuzzcaseSets:
                
                caseSetRunSummaryId = shortuuid.uuid()
                
                self.dbLock.acquire()
                
                create_casesetrun_summary(Id = caseSetRunSummaryId,
                                          fuzzCaseSetId=  fcs.Id,
                                          fuzzCaseSetRunId = self.fuzzCaseSetRunId,
                                          fuzzcontextId = self.apifuzzcontext.Id,
                                          totalRunsToComplete = self.totalFuzzRuns)
                self.dbLock.release()
                
                for _ in range(self.apifuzzcontext.fuzzcaseToExec):

                    future = self.executor.submit(self.fuzz_each_fuzzcaseset, caseSetRunSummaryId, fcs )#, self.fuzzCaseSetRunId, caseSetRunSummaryId, fcs )
                    
                    future.add_done_callback(self.fuzzcaseset_done)      
                    
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
        
    def fuzz_each_fuzzcaseset(self, caseSetRunSummaryId, fcs: ApiFuzzCaseSet):
        
        try:
            fuzzDataCase = self.http_call_api(fcs)
            
            summaryViewModel = self.save_fuzzDataCase(caseSetRunSummaryId, fuzzDataCase)
            
            #send data to GUI pver websocket
            self.eventstore.feedback_client('fuzz.update.casesetrunsummary', summaryViewModel)
            self.eventstore.feedback_client('fuzz.update.fuzzdatacase', fuzzDataCase)
            
        except Exception as e:
            if self.fuzzCancel == True:
                return
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzz_each_fuzzcaseset')
            
    def http_call_api(self, fcs: ApiFuzzCaseSet) -> ApiFuzzDataCase:
    
        try:
        
            fuzzDataCase = self.create_fuzzdatacase(fuzzcaseSetId=fcs.Id,
                                                    fuzzcontextId=self.apifuzzcontext.Id)
            
            ok, err, hostname, port, hostnamePort, url, path, querystring, body, headers, files = self.dataprep_fuzzcaseset( self.apifuzzcontext, fcs)
            
            # problem exist in fuzz data preparation, cannot continue.
            if not ok:
                raise(Exception('Error at data prep when fuzzing: {err}'))
            
            
            req: Request = None
            resp: Response = None
            httpSession = Session()
            
            if len(files) > 0:
                req = Request(fcs.verb, url, headers=headers, json=body, files=files)
            else:
                req = Request(fcs.verb, url, headers=headers, json=body)
                
            prepReq = req.prepare()
            
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
                                    body=body,
                                    contentLength=reqContentLength)
            
            resp = httpSession.send(prepReq, timeout=self.httpTimeoutInSec, verify=False)
            
            fuzzResp = self.create_fuzz_response(self.apifuzzcontext.Id, fuzzDataCase.Id, resp)
            
            fuzzDataCase.response = fuzzResp
            
            self.save_resp_cookie_if_exists(hostnamePort, fuzzResp.setcookieHeader)          
            
    
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
            
            # when cancelled during http call due to user cancelling and executor being shutdown,
            # error will occured, just ignore
            if self.fuzzCancel == True:
                return
            
            fr = ApiFuzzResponse()
            fr.Id = shortuuid.uuid()
            fr.datetime = datetime.now()
            fr.fuzzcontextId = self.apifuzzcontext.Id
            fr.fuzzDataCaseId = fuzzDataCase.Id
                
            if resp != None:
                fr.statusCode = resp.status_code
                fr.reasonPharse = resp.reason
                fr.body = resp.text
            else:  
                err =  Utils.jsone(e.args)
                fr.statusCode = 400 if err.find('timed out') == -1 else 508 #400 client error
                fr.reasonPharse = f'{err}'
            
            fuzzDataCase.response = fr
            
        return fuzzDataCase
            
                
    def fuzzcaseset_done(self, future):
        
        try:
            if self.fuzzCancel:
                return
            
            self.currentFuzzRuns = self.currentFuzzRuns + 1
            
            print(f'fuzz runs: {self.currentFuzzRuns}/{self.totalFuzzRuns}')
    
            # check if last task, to end fuzzing
            if self.currentFuzzRuns  >= self.totalFuzzRuns:
                
                self.dbLock.acquire()
                
                update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId)
                
                self.dbLock.release()
                
                self.eventstore.feedback_client('fuzz.complete', '')
                
                # notify fuzzing started
                pub.sendMessage(self.eventstore.FuzzingStartEventTopic, command='fuzzing_stop', msgData=self.apifuzzcontext.Id)
                
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzzcaseset_done')
        

    def save_fuzzDataCase(self, caseSetRunSummaryId, fdc: ApiFuzzDataCase) -> ApiFuzzCaseSets_With_RunSummary_ViewModel:
    
        try:
            
            self.dbLock.acquire()
            
            insert_api_fuzzdatacase(self.fuzzCaseSetRunId, fdc)
            
            insert_api_fuzzrequest(fdc.request)
            
            insert_api_fuzzresponse(fdc.response)
            
            # update run summary
            summaryViewModel = update_casesetrun_summary(fdc.fuzzcontextId, fdc.fuzzCaseSetId, caseSetRunSummaryId,
                                      int(fdc.response.statusCode),
                                      completedDataCaseRuns=1)
            
            self.dbLock.release()
            
            return summaryViewModel
            
        except Exception as e:
            #error occurs when fuzzing cancel, if is cancelled, ignore error
            if not self.fuzzCancel is True:
                ej = Utils.jsone(e)
                self.eventstore.emitErr(f'Error when saving fuzzdatacase, fuzzrequest and fuzzresponse: {ej}', data='WebApiFuzzer.save_fuzzDataCase')
                
    
    def create_fuzzrequest(self, fuzzDataCaseId, fuzzcontextId, hostname, port, hostnamePort, verb, path, qs, url, headers, body, contentLength):
        
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
            fr.body = body
            fr.contentLength = contentLength
            
            headerMultilineText = ''
            
            if type(headers) is dict and len(headers) > 0:
                for x in headers.keys():
                    headerMultilineText = headerMultilineText + f'{x}:{headers[x]}\n'
                
            fr.requestMessage = f'{fr.verb} {fr.url}' \
                                 '\n' \
                                 '\n' \
                                f'{headerMultilineText}' \
                                 '\n' \
                                f'{fr.body if fr.body != "{}" else ""}'
            
            return fr
        
        except Exception as e:
            ej = Utils.jsone(e)
            self.eventstore.emitErr(f'Error when saving fuzzdatacase, fuzzrequest and fuzzresponse: {ej}', data='WebApiFuzzer.create_fuzzrequest')
        
            
    def create_fuzz_response(self, fuzzcontextId, fuzzDataCaseId, resp: Response) -> ApiFuzzResponse:
    
        fuzzResp = ApiFuzzResponse()
        
        fuzzResp.Id = shortuuid.uuid()
        fuzzResp.datetime = datetime.now()
        fuzzResp.fuzzDataCaseId = fuzzDataCaseId
        fuzzResp.fuzzcontextId = fuzzcontextId 
        
        fuzzResp.statusCode = resp.status_code
        fuzzResp.reasonPharse = resp.reason
        fuzzResp.body = resp.text #.decode('utf-8')
        
        headers = {}
        headersMultilineText = ''
        for k in resp.headers.keys():
            headers[k] = resp.headers[k]
            headersMultilineText = headersMultilineText + f'{k}: {resp.headers[k]}\n'
            
        fuzzResp.headersJson = Utils.jsone(headers)
            
        fuzzResp.setcookieHeader = self.try_get_setcookie_value(headers)
        
        fuzzResp.contentLength = resp.headers['Content-Length']
        
        fuzzResp.responseDisplayText = f'{fuzzResp.statusCode} {fuzzResp.reasonPharse}' \
                                       f'{headersMultilineText}' \
                                       '\n' \
                                       '\n' \
                                       f'Date: {fuzzResp.datetime.strftime("%d/%m/%y %H:%M:%S.%f")}' \
                                       '\n' \
                                       f'Content-Length: {fuzzResp.contentLength}' \
                                       '\n' \
                                       '\n' \
                                       f'{fuzzResp.body}'
        
        return fuzzResp
    
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
            hostname = fc.hostname
            port = fc.port
            hostnamePort = fc.get_hostname_port()
            pathDT = fcs.get_path_datatemplate()
            querystringDT = fcs.querystringDataTemplate
            bodyDT= fcs.bodyDataTemplate
            headerDT = fcs.headerDataTemplate
            files = {} #single file only for openapi3
            
            okpath, errpath, resolvedPathDT = self.corporaContext.resolve_expr(pathDT) #self.inject_fuzzdata_in_datatemplate(pathDT)
            if not okpath:
                return [False, errpath, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            okqs, errqs, resolvedQSDT = self.corporaContext.resolve_expr(querystringDT) #self.inject_fuzzdata_in_datatemplate(querystringDT)
            if not okqs:
                return [False, errqs, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            okbody, errbody, resolvedBodyDT = self.corporaContext.resolve_expr(bodyDT) #self.inject_fuzzdata_in_datatemplate(bodyDT)
            if not okbody:
                return [False, errbody, hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers]
            
            if len(fcs.file) > 0:
                for fileType in fcs.file:
                    ok, err, fileContent = self.corporaContext.resolve_file(fileType)
                    if ok:
                        filename = self.corporaContext.cp.fileNameCorpora.next_corpora()
                        files[filename] = fileContent   # list of tuple file names and binary content
            
            
            # header - reason for looping over each header data template and getting fuzz data is to 
            # prevent json.dump throwing error from Json reserved characters 
            headerDict = {}
            headerDTObj = jsonpickle.decode(headerDT, safe=False, keys=False)
            for hk in headerDTObj.keys():
                dt = headerDTObj[hk]
                
                ok, err, resolvedVal = self.corporaContext.resolve_expr(dt) #self.inject_fuzzdata_in_datatemplate(dataTemplate)
                if not ok:
                    self.eventstore.emitErr(err, 'webapi_fuzzer.dataprep_fuzzcaseset')
                    continue
                
                headerDict[hk] = resolvedVal
                
            
            if len(files) > 0:
                headerDict["Content-Type"] = "multipart/form-data"
            
            url = f'{hostnamePort}{resolvedPathDT}{resolvedQSDT}'
            
            authnHeader= self.determine_authn_scheme(fc)
                    
            headers = {**authnHeader, **headerDict}     #merge 2 dicts
            
            return [True, '', hostname, port, hostnamePort, url, resolvedPathDT, resolvedQSDT, resolvedBodyDT, headers, files]
        
        except Exception as e:
            errText =  Utils.errAsText(e)
            self.eventstore.emitErr(f'Error {errText}', data='WebApiFuzzer.dataprep_fuzzcaseset')
            return False, errText
    
    def create_http_headers(self):
        pass
    
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
    