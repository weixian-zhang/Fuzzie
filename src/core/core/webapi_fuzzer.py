
# supported type expression
# openapi3 types
    # {{ string }}                  this includes dates and files
    # {{ number }}                  treated as Fuzzie digit
    # {{ integer }}                 treated as Fuzzie digit
    # {{ boolean }}
# in addition, input expression for Request Message
    # {{ my:[myvalue1,myvalue2,3,4] }}  # supply your own input
    # {{ mutate:[a quick brown fox, Whatever you are, be a good one] }}   # mutates by per char add/alter/remove mutations
    # {{ string }}                  
    # {{ number }}                  
    # {{ file }}
    # {{ boolean }}
    # {{ datetime }}
    # {{ username }}                for login bruteforce entry test
    # {{ password }}                for login bruteforce entry test
    # {{ digit }}                   integer and float
    # {{ char }}
    # {{ base64e:value }}
    # {{ base64e }}                 generate base64 encoded random string value
    # {{ hashsha256:value }}        generates a sha256 hash from supplied value

import jsonpickle
from utils import Utils
from cProfile import run
from cmath import pi
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
import urllib3 
from pubsub import pub
from http import cookiejar
from types import MappingProxyType
import jinja2
import httplib2
import json
import sys
import shortuuid
from datetime import datetime
from eventstore import EventStore, MsgType
from datafactory.hacked_password_generator import HackedPasswordGenerator
from datafactory.hacked_username_generator  import HackedUsernameGenerator
from datafactory.naughty_file_generator import NaughtyFileGenerator
from datafactory.naughty_datetime_generator import NaughtyDateTimeGenerator
from datafactory.naughty_digits_generator import NaughtyDigitGenerator
from datafactory.naughty_string_generator import NaughtyStringGenerator
from datafactory.naughty_bool_generator import NaughtyBoolGenerator
from datafactory.obedient_data_generators import ObedientCharGenerator 
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

class ThreadTracker(dict):
    
    def __init__(self, all_tasks_completed_callback, *args, **kwargs):
        self.all_tasks_completed_callback = all_tasks_completed_callback
        self.update(*args, **kwargs)
    
    def __delitem__(self, key):
        print(f'{key} is being poped')
        
        if dict.__len__ == 0:
            self.all_tasks_completed_callback()
            
        del self.store[self._keytransform(key)]
        
        

class WebApiFuzzer:
    
    def __init__(self,
                    dataQueue,
                    apifuzzcontext: ApiFuzzContext,
                    basicUsername = '',
                    basicPassword = '',
                    bearerTokenHeader = 'Authorization',
                    bearerToken = '',
                    apikeyHeader = '',
                    apikey = '') -> None:
        
        # supports remember Set-Cookie from response
        #cookie example
        # contain in single header = cookie1=value1;cookie2=value2
        # Set-Cookie: chocolate=chips; expires=Sun, 15-Nov-2009 18:47:08 GMT; path=/; domain=thaorius.net; secure; httponly
        # Set-Cookie: milk=shape
        self.cookiejar = {}
        
        self.dataQueue = dataQueue
        
        # security creds
        self.basicUsername = basicUsername,
        self.basicPassword = basicPassword,
        self.bearerTokenHeader = bearerTokenHeader,
        self.bearerToken = bearerToken,
        self.apikeyHeader = apikeyHeader,
        self.apikey = apikey
        
        self.http = urllib3.PoolManager(num_pools=5)
        self.httpTimeoutInSec = 3.0
        self.fuzzCancel = False
        self.fuzzCaseSetRunId = shortuuid.uuid()
        self.totalFuzzRuns = 0
        self.currentFuzzRuns = 0
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        self.processLock = Lock()
        self.dbLock = Lock()
        
        self.eventstore = EventStore()
        self.apifuzzcontext = apifuzzcontext
        self.passwordGenerator = HackedPasswordGenerator()
        self.usernameGenerator = HackedUsernameGenerator()
        self.fileGenerator = NaughtyFileGenerator() 
        self.datetimeGenerator = NaughtyDateTimeGenerator() 
        self.digitGenerator = NaughtyDigitGenerator() 
        self.stringGenerator = NaughtyStringGenerator() 
        self.boolGenerator = NaughtyBoolGenerator() 
        self.usernameGenerator = HackedUsernameGenerator()
        self.CharGenerator = ObedientCharGenerator()
        
        pub.subscribe(self.pubsub_command_receiver, 'command_relay')


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
            
            fuzzCasesToTest = self.determine_no_of_fuzzcases_to_run(self.apifuzzcontext.fuzzMode, self.apifuzzcontext.fuzzcaseToExec)
            
            # create a fuzzcaserun record
            self.dbLock.acquire()
            insert_api_fuzzCaseSetRuns(self.fuzzCaseSetRunId, self.apifuzzcontext.Id)
            self.dbLock.release()
            
            # fuzzCasesToTest = 1 # uncomment for testing only
            self.totalFuzzRuns = len(self.apifuzzcontext.fuzzcaseSets) * fuzzCasesToTest
            
            for fcs in self.apifuzzcontext.fuzzcaseSets:
                
                caseSetRunSummaryId = shortuuid.uuid()
                
                self.dbLock.acquire()
                create_casesetrun_summary(Id = caseSetRunSummaryId,
                                          fuzzCaseSetId=  fcs.Id,
                                          fuzzCaseSetRunId = self.fuzzCaseSetRunId,
                                          fuzzcontextId = self.apifuzzcontext.Id,
                                          totalRunsToComplete = self.totalFuzzRuns)   
                self.dbLock.release()           
                
                for count in range(0, fuzzCasesToTest):

                    future = self.executor.submit(self.fuzz_data_case, self.fuzzCaseSetRunId, caseSetRunSummaryId, fcs )
                    
                    future.add_done_callback(self.fuzz_data_case_done)      
                    
        except Exception as e:
            self.eventstore.emitErr(e, data='begin_fuzzing')
        
    def fuzz_data_case(self, fuzzCaseSetRunId, caseSetRunSummaryId, fcs: ApiFuzzCaseSet):
        
        try:
            fuzzDataCase = self.http_call_api(fcs)
            
            summaryViewModel = self.save_fuzzDataCase(caseSetRunSummaryId, fuzzDataCase)
            
            self.dataQueue.put(Utils.jsone(summaryViewModel))
            
            
        except Exception as e:
            if self.fuzzCancel == True:
                return
            self.eventstore.emitErr(e, data='fuzz_data_case')
            
    def http_call_api(self, fcs: ApiFuzzCaseSet) -> ApiFuzzDataCase:
    
        try:
            
                
            fuzzDataCase = self.create_fuzzdatacase(fuzzcaseSetId=fcs.Id,
                                                    fuzzcontextId=self.apifuzzcontext.Id)
            
            OK, hostnamePort, url, path, querystring, body, headers = self.dataprep_fuzzcaseset( self.apifuzzcontext, fcs)
            
            # problem exist in fuzz data preparation, cannot continue.
            if not OK:
                return
            
            fuzzDataCase.request = self.create_fuzzrequest(
                                    fuzzDataCaseId=fuzzDataCase.Id,
                                    fuzzcontextId=self.apifuzzcontext.Id,
                                    hostnamePort=hostnamePort,
                                    url=url,
                                    path=path,
                                    qs=querystring,
                                    verb=fcs.verb,
                                    headers=headers,
                                    body=body)
            
            
            resp = self.http.request(fcs.verb, url, headers=headers, body=body, retries=False, timeout=self.httpTimeoutInSec)
            
            fuzzResp: ApiFuzzResponse= self.create_fuzz_response(self.apifuzzcontext.Id, fuzzDataCase.Id, resp)
            
            fuzzDataCase.response = fuzzResp 
            
            self.save_resp_cookie_if_exists(hostnamePort, fuzzResp.setcookieHeader)
    
        except HTTPError as e:
            
            err = Utils.jsone(e.args)
            
            fr = ApiFuzzResponse()
            fr.Id = shortuuid.uuid()
            fr.datetime = datetime.now()
            fr.fuzzcontextId = self.apifuzzcontext.Id
            fr.fuzzDataCaseId = fuzzDataCase.Id
            fr.statusCode = 500
            fr.reasonPharse = err
            fuzzDataCase.response = fr
            
        except Exception as e:
            
            # when cancelled during http call due to user cancelling and executor being shutdown,
            # error will occured, just ignore
            if self.fuzzCancel == True:
                return
            
            err =  Utils.jsone(e.args)
                
            fr = ApiFuzzResponse()
            fr.Id = shortuuid.uuid()
            fr.datetime = datetime.now()
            fr.fuzzcontextId = self.apifuzzcontext.Id
            fr.fuzzDataCaseId = fuzzDataCase.Id
            fr.statusCode = 500 if err.find('timed out') == -1 else 508
            fr.reasonPharse = f'{err}'
            fuzzDataCase.response = fr
            
        return fuzzDataCase
    
    def fuzz_data_case_done(self, future):
        
        try:
            self.currentFuzzRuns = self.currentFuzzRuns + 1
            
            print(f'fuzz runs: {self.currentFuzzRuns}/{self.totalFuzzRuns}')
    
            # check if last task, to end fuzzing
            if self.totalFuzzRuns == 0:
                self.dbLock.acquire()
                update_api_fuzzCaseSetRun_status(self.fuzzCaseSetRunId)
                self.dbLock.release()
                self.eventstore.send_websocket('fuzzing is completed')
                
        except Exception as e:
            self.eventstore.emitErr(e, data='fuzz_data_case_done')
        

    def save_fuzzDataCase(self, caseSetRunSummaryId, fdc: ApiFuzzDataCase) -> ApiFuzzCaseSets_With_RunSummary_ViewModel:
    
        try:
            
            self.dbLock.acquire()
            
            insert_api_fuzzdatacase(self.fuzzCaseSetRunId, fdc)
            
            insert_api_fuzzrequest(fdc.request)
            
            insert_api_fuzzresponse(fdc.response)
            
            # update run summary
            summaryViewModel = update_casesetrun_summary(caseSetRunSummaryId,
                                      int(fdc.response.statusCode),
                                      completedDataCaseRuns=1)
            
            self.dbLock.release()
            
            return summaryViewModel
            
        except Exception as e:
            #error occurs when fuzzing cancel, if is cancelled, ignore error
            if not self.fuzzCancel is True:
                ej = Utils.jsone(e)
                self.eventstore.emitErr(f'Error when saving fuzzdatacase, fuzzrequest and fuzzresponse: {ej}', data='save_fuzzDataCase')
                
    
    def create_fuzzrequest(self, fuzzDataCaseId, fuzzcontextId, hostnamePort, verb, path, qs, url, headers, body):
        
        try:
            fr = ApiFuzzRequest()
        
            fr.Id = shortuuid.uuid()
            fr.datetime = datetime.now()
            fr.fuzzDataCaseId = fuzzDataCaseId
            fr.fuzzcontextId =fuzzcontextId
            fr.hostnamePort = hostnamePort
            fr.verb = verb
            fr.path = path
            fr.querystring = qs
            fr.url = url
            fr.headers = Utils.jsone(headers)
            fr.body = body
            
            headerMultilineText = ''
            
            if type(headers) is dict and len(headers) > 0:
                for x in headers.keys():
                    headerMultilineText = headerMultilineText + f'{x}:{headers[x]}\n'
                
            fr.requestMessage = f'''
            {fr.verb} {fr.path} HTTP/1.1
            {headerMultilineText}

            {fr.body if fr.body != '{}' else ''}
            '''
            
            return fr
        
        except Exception as e:
            ej = Utils.jsone(e)
            self.eventstore.emitErr(f'Error when saving fuzzdatacase, fuzzrequest and fuzzresponse: {ej}', data='create_fuzzrequest')
        
            
    def create_fuzz_response(self, fuzzcontextId, fuzzDataCaseId, resp) -> ApiFuzzResponse:
    
        fuzzResp = ApiFuzzResponse()
        
        fuzzResp.Id = shortuuid.uuid()
        fuzzResp.datetime = datetime.now()
        fuzzResp.fuzzDataCaseId = fuzzDataCaseId
        fuzzResp.fuzzcontextId = fuzzcontextId 
        
        fuzzResp.statusCode = resp.status
        fuzzResp.reasonPharse = resp.reason
        fuzzResp.body = resp.data.decode('utf-8')
        
        headers = {}
        headersMultilineText = ''
        for k in resp.headers.keys():
            headers[k] = resp.headers[k]
            headersMultilineText = headersMultilineText + f'{resp.headers[k]}\n'
            
        fuzzResp.headersJson = Utils.jsone(headers)
            
        fuzzResp.setcookieHeader = self.try_get_setcookie_value(headers)
        
        fuzzResp.responseDisplayText = f'''
            # HTTP/1.1 {fuzzResp.statusCode} {fuzzResp.reasonPharse}
              {headersMultilineText}
              
              {fuzzResp.body}
        '''
        
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
            hostnamePort = fc.get_hostname_port()
            pathDT = fcs.get_path_datatemplate()
            querystringDT = fcs.querystringDataTemplate
            bodyDT= fcs.bodyDataTemplate
            headerDT = fcs.headerDataTemplate
            
            path = self.inject_fuzzdata_in_datatemplate(pathDT)
            querystring = self.inject_fuzzdata_in_datatemplate(querystringDT)
            body = self.inject_fuzzdata_in_datatemplate(bodyDT)
            
            # header - reason for looping over each header data template and getting fuzz data is to 
            # prevent json.dump throwing error from Json reserved characters 
            headerDict = {}
            headerDTObj = jsonpickle.decode(headerDT, safe=False, keys=False)
            for hk in headerDTObj.keys():
                dataTemplate = headerDTObj[hk]
                transformedValue = self.inject_fuzzdata_in_datatemplate(dataTemplate)
                headerDict[hk] = transformedValue
                
            # headerStr = self.inject_fuzzdata_in_datatemplate(headerDT)
            # headerDict = jsonpickle.decode(headerStr, safe=False, keys=False)
            
            url = f'{hostnamePort}{path}{querystring}'
            
            authnHeader= self.determine_authn_scheme(fc)
                    
            headers = {**authnHeader, **headerDict}     #merge 2 dicts
            
            return [True, hostnamePort, url, path, querystring, body, headers]
        
        except Exception as e:
            ej =  Utils.jsone(e)
            self.eventstore.emitErr(f'{ej}', data='Fuzzer/DataPrep')
            return [False]
        
    
    # returns dict representing header
    def determine_authn_scheme(self, fc: ApiFuzzContext) -> dict:
        securityHeaders = {}
        
        if fc.authnType == SupportedAuthnType.Anonymous.name:
            return {}
        
        if fc.authnType == SupportedAuthnType.Basic.name:
            return {
                    'Authorization': f'Basic {self.basicUsername}:{self.basicPassword}'
                   }
        
        elif fc.authnType == SupportedAuthnType.Bearer.name:
            return {
                    f'{fc.bearerTokenHeader}': f'{fc.bearerToken}'
                   }

        elif fc.authnType == SupportedAuthnType.ApiKey.name:
            
            return {
                    f'{fc.apikeyHeader}': f'{fc.apikey}'
                   }
            
        return {}
            
    def inject_fuzzdata_in_datatemplate(self, tpl: str) -> str:
        
        if tpl == '':
            return ''
        
        template = jinja2.Template(tpl)
        result =  template.render({ 'getFuzzData': self.getFuzzData })
        return result
            
    def getFuzzData(self, type: str):
        
        if type is None:
            return self.stringGenerator.NextData() 
        match type._undefined_name:
            case 'string':
                return self.stringGenerator.NextData()
            case 'number':
                return self.digitGenerator.NextData()
            case 'integer':
                return self.digitGenerator.NextData()
            case 'int':
                return self.digitGenerator.NextData()
            case 'digit':
                return self.digitGenerator.NextData()
            case 'bool':
                return self.boolGenerator.NextData()
            case 'username':
                return self.usernameGenerator.NextData()
            case 'password':
                return self.passwordGenerator.NextData()
            case 'char':
                return self.CharGenerator.NextData()
            case 'datetime':
                return self.datetimeGenerator.NextData()
            case 'file':
                return self.fileGenerator.NextData()
            case _:
                return self.stringGenerator.NextData()
    

        
    
    def create_fuzzdatacase(self, fuzzcaseSetId, fuzzcontextId):
        
        fdc = ApiFuzzDataCase()
        fdc.Id = shortuuid.uuid()
        fdc.fuzzCaseSetId = fuzzcaseSetId
        fdc.fuzzcontextId = fuzzcontextId
        return fdc

         
        
        
    # minimum 100 fuzz cases to run
    def determine_no_of_fuzzcases_to_run(self, fuzzmode: str, fuzzcaseToExec):
        
        default = 100
        
        if fuzzmode == FuzzMode.Quick.name:
            return default
        elif fuzzmode == FuzzMode.Full.name:
            return self.stringGenerator.get_dbsize()
        elif fuzzmode == FuzzMode.Custom.name:
            if fuzzcaseToExec <= default:
                return default
            else:
                return fuzzcaseToExec
    