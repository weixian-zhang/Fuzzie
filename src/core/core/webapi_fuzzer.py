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
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urlparse
from types import MappingProxyType
import shortuuid
from collections import OrderedDict
from datetime import datetime
from eventstore import EventStore, MsgType
from fuzz_test_result_queue import FuzzTestResultQueue
from models.apicontext import SupportedAuthnType
from models.webapi_fuzzcontext import (ApiFuzzContext, ApiFuzzCaseSet, ApiFuzzDataCase, 
                                       ApiFuzzRequest, ApiFuzzResponse, FuzzTestResult,
                                        FuzzMode, FuzzCaseSetFile, WordlistType)
from graphql_models import ApiFuzzCaseSets_With_RunSummary_ViewModel
from corporafactory.corpora_context_builder import CorporaContextBuilder
from template_helper import TemplateHelper

import re

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
import requests.utils 
import traceback

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
        
        #request config
        requests.adapters.DEFAULT_RETRIES = 1
        
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
        
        self.httpTimeoutInSec = 3.0
        self.fuzzCaseSetRunId = shortuuid.uuid()
        
        self.totalRunsForAllCaseSets = 0
        self.totaRunsPerCaseSet = 0
        
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        self.multithreadEventSet = Event()
        
        self.corporaContext = CorporaContext()
        
        self.corporaContextBuilder = CorporaContextBuilder(self.corporaContext)
        
        self.eventstore = EventStore()
        self.apifuzzcontext = apifuzzcontext
    
        
    def __del__(self):
        
        tb = traceback.format_exc()
        print(tb)
    
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
    
    
    def fuzz_once(self, fuzzcasesetId):
        
        try:
            
            ok, err = self.corporaContextBuilder.build_for_api(self.apifuzzcontext.fuzzcaseSets)
            if not ok:
                raise Exception(err)
            
            insert_api_fuzzCaseSetRuns(self.fuzzCaseSetRunId, self.apifuzzcontext.Id)
                        
            self.fuzzingStatus = FuzzingStatus.Fuzzing
            
            self.executor.submit(self.fuzz_once_in_worker_thread, fuzzcasesetId)               
                    
            return self.fuzzCaseSetRunId #caseSetRunSummaryId
                    
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.begin_fuzzing')
        finally:
                       
            self.totaRunsPerCaseSet = 0
            
            self.fuzzingStatus = FuzzingStatus.Stop
            
    def fuzz_once_in_worker_thread(self, fuzzcasesetId):
        
        try:
            fcsLen = len(self.apifuzzcontext.fuzzcaseSets)
            
            if fcsLen == 0:
                self.eventstore.emitErr(f"no fuzz case detected for fuzz-context {self.apifuzzcontext.name}, fuzzing stopped")
                return
            
            caseSetRunSummaryId = shortuuid.uuid()
            self.apifuzzcontext.fuzzcaseToExec = 1
            self.totaRunsPerCaseSet = 1
            self.totalRunsForAllCaseSets = 1
            
            for fcs in self.apifuzzcontext.fuzzcaseSets:
                
                if fcs.Id == fuzzcasesetId:
                    
                    create_runsummary_per_fuzzcaseset(Id = caseSetRunSummaryId,
                                            fuzzCaseSetId=  fcs.Id,
                                            fuzzCaseSetRunId = self.fuzzCaseSetRunId,
                                            fuzzcontextId = self.apifuzzcontext.Id,
                                            totalRunsToComplete = self.totaRunsPerCaseSet)
                
                    self.fuzz_each_fuzzcaseset(caseSetRunSummaryId, fcs, self.multithreadEventSet, runNumber=1)

        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzz_once_in_worker_thread')
            
        
    async def fuzz(self):
        
        if self.apifuzzcontext == None or len(self.apifuzzcontext.fuzzcaseSets) == 0:
            self.eventstore.emitErr(f'WebApiFuzzer detected empty ApiFuzzContext: {self.apifuzzcontext}')
            return
        
        await self.begin_fuzzing()
        
    async def begin_fuzzing(self):
          
        try:
            
            ok, err = self.corporaContextBuilder.build_for_api(self.apifuzzcontext.fuzzcaseSets)
            if not ok:
                raise Exception(err)
            
            insert_api_fuzzCaseSetRuns(self.fuzzCaseSetRunId, self.apifuzzcontext.Id)
                        
            self.fuzzingStatus = FuzzingStatus.Fuzzing
            
            fcsLen = len(self.apifuzzcontext.fuzzcaseSets)
            
            if fcsLen == 0:
                self.eventstore.emitErr(f"no fuzz case detected for fuzz-context {self.apifuzzcontext.name}, fuzzing stopped")
                return
            
            self.executor.submit(self.begin_fuzzing_in_worker_thread)
                    
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.begin_fuzzing')
            
    def begin_fuzzing_in_worker_thread(self):
        
        try:
            
            fcsLen = len(self.apifuzzcontext.fuzzcaseSets)
        
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
                    
            self.executor.submit(self.fuzz_completion_monitor)
            
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.begin_fuzzing_in_worker_thread')
            
        
    def fuzz_completion_monitor(self):
        
        while len(FuzzTestResultQueue.resultQueue) > 0:
            time.sleep(1)
        
        self.fuzzingStatus = FuzzingStatus.Stop
        
        update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId)
                
        self.multithreadEventSet.set()
    
        self.executor.shutdown(wait=False, cancel_futures=True)
        
        self.totaRunsPerCaseSet = 0
        
          
    def fuzz_each_fuzzcaseset(self, caseSetRunSummaryId, fcs: ApiFuzzCaseSet, multithreadEventSet: Event, runNumber: int):
        
        try:
            
            # for cancel fuzzing
            if multithreadEventSet.is_set():
                return
            
            fuzzDataCase, file = self.http_call(fcs)
            
            self.enqueue_fuzz_result_for_persistent(caseSetRunSummaryId, fuzzDataCase, file)
            
        except Exception as e:
            errMsg = Utils.errAsText(e)
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzz_each_fuzzcaseset')
            self.cancel_fuzzing(errorMsg=errMsg)
            
    def http_call(self, fcs: ApiFuzzCaseSet) -> tuple([ApiFuzzDataCase, dict]):
        
        resp = None
        ok = True
        err = ''
        hostname=''
        port=443
        hostnamePort=''
        url=''
        path=''
        querystring=''
        body=''
        headers={}
        file = ''
        gqlVars = {}
        
        try:
            
            fuzzDataCase = self.create_fuzzdatacase(fuzzcaseSetId=fcs.Id,
                                                    fuzzcontextId=self.apifuzzcontext.Id)
            
            # url already includes hostname, port, path and qs
            # files = list[tuple(wordlistType, filename, content)]
            (ok, 
             err, 
             hostname, 
             port, 
             hostnamePort, 
             url, 
             path, 
             querystring,
             body,
             headers,
             file,
             gqlVars) = self.dataprep_fuzzcaseset( self.apifuzzcontext, fcs)
            
            
            # problem exist in fuzz data preparation, cannot continue.
            if not ok:
                self.eventstore.emitErr(Exception('Error at data prep when fuzzing: {err}'))
                raise Exception(err)
    
            
            try:
                req = None                
                
                # post with body multipart-form, www-form-urlencoded
                if body != '':
                    
                    if fcs.isGraphQL:
                        req = Request('POST', url, headers=headers, json={"query": body, 'variables': gqlVars})
                        body = f'{body}\n\n{Utils.jsone(gqlVars)}'
                    else:
                        req = Request(fcs.verb, url, headers=headers, data=body) 

                # upload file
                # support single file only.
                # intention is to upload file content as the entire POST body.
                # with multiple files being uploaded, multipart-form headers Content-Disposition will be included as file content.
                # which fuzzie tries to avoid altering original file content
                elif fcs.has_file_to_upload():
                    
                    req = Request(fcs.verb, url, headers=headers, data=file.content)
                else:
                    req = Request(fcs.verb, url, headers=headers)
                
                
                # override requests-library "legal header" check to allow any chars
                # original regex is commented
                requests.utils._CLEAN_HEADER_REGEX_STR = re.compile(r'(.*?)') #re.compile(r'^\S[^\r\n]*$|^$')
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
                        body=body,
                        contentLength=reqContentLength)
                
    
                # make http request
                try:
                    retry_strategy  = Retry(total=False)
                    adapter = HTTPAdapter(max_retries=retry_strategy)
                    session = requests.Session()
                    session.mount('https://', adapter)
                    session.mount('http://', adapter)                    
                   
                    resp = session.send(prepReq, timeout=self.httpTimeoutInSec, allow_redirects=False, verify=False) #timeout=self.httpTimeoutInSec, allow_redirects=False, verify=False)
                
                except Exception as e:
                    
                    errMsg = Utils.errAsText(e)
                    
                    fuzzResp = self.create_fuzz_response_on_error(self.apifuzzcontext.Id, 
                                                                   fuzzDataCase.Id, 
                                                                   reason= errMsg)
                    fuzzDataCase.response = fuzzResp
                    return fuzzDataCase, file
                
            
            except Exception as e:
                self.eventstore.emitErr(e)
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
                                        body=body,
                                        contentLength=0,
                                        invalidRequestError=err)
                fuzzResp = self.create_fuzz_response_on_error(self.apifuzzcontext.Id, 
                                                                   fuzzDataCase.Id, 
                                                                   reason=err)
                fuzzDataCase.response = fuzzResp
                
                return fuzzDataCase, ''
            
            
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
            err = Utils.errAsText(e)
            
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
                                        contentLength=0,
                                        invalidRequestError=err)
            
            resp = self.create_fuzz_response_on_error(self.apifuzzcontext.Id, 
                                                                   fuzzDataCase.Id, 
                                                                   reason=err)
            resp.statusCode = 400
            
            fuzzDataCase.response = resp
            
            return fuzzDataCase, ''
            
        return fuzzDataCase, file
    
    
    
    def create_erroreous_fuzzdatacase():
        pass
        
             
    def fuzzcaseset_done(self, runNumber):
        
        try:
                
            # check if last task, to end fuzzing
            if runNumber >= self.totalRunsForAllCaseSets:
                
                update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId)
                
                self.multithreadEventSet.set()
            
                self.executor.shutdown(wait=False, cancel_futures=True)
                
                self.totaRunsPerCaseSet = 0
                
                self.fuzzingStatus = FuzzingStatus.Stop
                
        except Exception as e:
            self.eventstore.emitErr(e, data='WebApiFuzzer.fuzzcaseset_done')

        
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
            
            # background task result saver is updating "run-statistics"
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
        
    def create_fuzz_response_on_error(self, fuzzcontextId, fuzzDataCaseId, reason='') -> ApiFuzzResponse:
        fuzzResp = ApiFuzzResponse()
        fuzzResp.Id = shortuuid.uuid()
        fuzzResp.datetime = datetime.now()
        fuzzResp.fuzzDataCaseId = fuzzDataCaseId
        fuzzResp.fuzzcontextId = fuzzcontextId 
        fuzzResp.statusCode = 408
        fuzzResp.reasonPharse = reason
        fuzzResp.responseDisplayText = Utils.b64e(reason) 
        return fuzzResp
     
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
                
            fuzzResp.headerJson = Utils.jsone(headers)
                
            fuzzResp.setcookieHeader = self.try_get_setcookie_value(headers)
            
            fuzzResp.contentLength = len(resp.content)
            
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
            
            url = ''
            hostname = ''
            port = 0
            hostnamePort = ''
            path = ''
            query = ''
            
            tplVars = fc.templateVariables
            
            urlDT= TemplateHelper.add_global_vars(vars=tplVars, tpl=fcs.urlDataTemplate)
            bodyDT= TemplateHelper.add_global_vars(vars=tplVars, tpl=fcs.bodyDataTemplate)
            myfileDT = TemplateHelper.add_global_vars(vars=tplVars, tpl=fcs.fileDataTemplate)
            file = ''
            resolvedBodyDT = ''
            headers = {}
            file = ''
            gqlVars = {}
            
            # get fuzz data for Url
            urlok, urlerr, renderedUrl = self.corporaContext.resolve_fuzzdata(urlDT) #self.inject_fuzzdata_in_datatemplate(pathDT)
            if not urlok:
                return [False, urlerr, hostname, port, hostnamePort, renderedUrl, path, query, resolvedBodyDT, headers, file, gqlVars]
            
            renderedUrl = renderedUrl.replace("\n", "").strip()
            
            if not Utils.validUrl(renderedUrl):
                return [False, f'invalid Url: {renderedUrl}', hostname, port, hostnamePort, renderedUrl, path, query, resolvedBodyDT, headers, file, gqlVars]
            
            
            # build Url parts
            parsedUrl = urlparse(renderedUrl)
            url = renderedUrl
            hostname = parsedUrl.hostname
            path = parsedUrl.path
            query = parsedUrl.query
            port = self.determine_port(parsedUrl.port, parsedUrl.scheme)
            hostnamePort = f'{hostname}:{port}'
            
            okbody, errbody, resolvedBodyDT = self.corporaContext.resolve_fuzzdata(bodyDT)
            
            _, resolvedBodyDT = Utils.try_decode_utf8(resolvedBodyDT)
            
            if not okbody:
                return [False, errbody, hostname, port, hostnamePort, url, path, query, resolvedBodyDT, headers, file, gqlVars]
            
            # header - reason for looping over each header data template and getting fuzz data is to 
            # prevent json.dump throwing error from Json reserved characters 
            headerDict = {}
            headerDTObj = Utils.try_parse_json_to_object(fcs.headerDataTemplate)
            
            if Utils.dict_has_items(headerDTObj):
                
                for key in headerDTObj.keys():
                    
                    valueDT = headerDTObj[key]
                    
                    headerKeyDT = TemplateHelper.add_global_vars(vars=tplVars, tpl=key)
                    
                    keyOK, keyErr, resolvedKey = self.corporaContext.resolve_fuzzdata(headerKeyDT)
                    if not keyOK:
                        self.eventstore.emitErr(keyErr, 'webapi_fuzzer.dataprep_fuzzcaseset')
                        continue
                    
                    headerValueDT = TemplateHelper.add_global_vars(vars=tplVars, tpl=valueDT)
                    
                    valOK, valErr, resolvedVal = self.corporaContext.resolve_fuzzdata(headerValueDT)
                    if not valOK:
                        self.eventstore.emitErr(valErr, 'webapi_fuzzer.dataprep_fuzzcaseset')
                        continue
                    
                    headerDict[resolvedKey] = resolvedVal
            
            # fuzzie custom header
            headerDict['User-Agent'] = 'fuzzie'
                    
            # handle file upload with "proper" encoding,
            # without encoding requests will throw error as requests uses utf-8 by default
            if fcs.has_file_to_upload():
                
                ok = True
                err = ''
                fileContent = ''
                fileWordlistType = fcs.file
                filename = ''
                
                if not Utils.isNoneEmpty(fcs.fileName):
                    filename = fcs.fileName
                else:
                    filename = self.corporaContext.cp.fileNameCorpora.next_corpora(fileType=fileWordlistType)
                
                if fileWordlistType == WordlistType.myfile:
                    
                    ok, err, fileContent = self.corporaContext.resolve_fuzzdata(myfileDT)
                    
                    if not ok:
                        return [False, err, hostname, port, hostnamePort, url, path, query, resolvedBodyDT, headers, file, gqlVars]
                    
                    _, decoded = Utils.try_decode_utf8(fileContent)
                    
                    file = FuzzCaseSetFile(wordlist_type=WordlistType.myfile, filename=filename, content=decoded)
                    
                # image, file, pdf
                else:
                    ok, err, fileContent = self.corporaContext.resolve_file(fcs.file)
                    
                    file = FuzzCaseSetFile(wordlist_type=fcs.file, filename=filename, content=fileContent)
            
            
            #graphql support
            if fcs.isGraphQL:
                gqlVarDT = TemplateHelper.add_global_vars(vars=tplVars, tpl=fcs.graphQLVariableDataTemplate)
                ok, err, gqlVariables = self.corporaContext.resolve_fuzzdata(gqlVarDT)
                gqlVars = Utils.try_parse_json_to_object(gqlVariables)
                
            
            authnHeader= self.determine_authn_scheme(fc)
                    
            headers = {**authnHeader, **headerDict}     #merge 2 dicts
            
            return [True, '', hostname, port, hostnamePort, url, path, query, resolvedBodyDT, headers, file, gqlVars]
        
        except Exception as e:
            errText =  Utils.errAsText(e)
            self.eventstore.emitErr(e, data='WebApiFuzzer.dataprep_fuzzcaseset')
            return [False, errText, hostname, port, hostnamePort, url, path, query, resolvedBodyDT, headers, file, gqlVars]
        
    def determine_port(self, port, scheme) -> int:
        if port is None:
            if scheme == 'http':
                return  80
            elif scheme == 'https':
                return 443
            else:
                return 443
        return port
    
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
    
    def is_grapgql(self, headers: dict):
        if Utils.isNoneEmpty(headers) or len(headers) == 0:
            return False
        
        xreqType = 'X-Request-Type'.lower()
        
        for k in headers.keys():
            if xreqType == k.lower():
                return True
       
        return False
    
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
    
    