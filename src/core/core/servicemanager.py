# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from api_discovery.requestmessage_fuzzcontext_creator import RequestMessageFuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext
from graphql_models import (ApiFuzzContext_Runs_ViewModel, 
                            ApiFuzzContextUpdate, 
                            ApiFuzzCaseSets_With_RunSummary_ViewModel,
                            FuzzRequest_ViewModel,
                            FuzzResponse_ViewModel,
                            FuzzDataCase_ViewModel,
                            WebApiFuzzerInfo,
                            FuzzRequestResponseMessage,
                            FuzzRequestFileUpload_ViewModel,
                            FuzzRequestFileUploadQueryResult,
                            FuzzRequestFileDownloadContentQueryResult)
from webapi_fuzzer import WebApiFuzzer, FuzzingStatus
from eventstore import EventStore, MsgType
from utils import Utils
from db import  (get_fuzzcontext,
                 get_caseSets_with_runSummary,
                 insert_db_fuzzcontext, 
                 update_api_fuzz_context,
                 delete_api_fuzz_context,
                 get_fuzzContexts_and_runs,
                 save_caseset_selected,
                 get_fuzz_request_response,
                 get_fuzz_request_response_messages,
                 get_uploaded_files,
                 get_uploaded_file_content)
from sqlalchemy.sql import select, insert
import base64
from pubsub import pub
import threading, time
from datetime import datetime
import queue

         
class ServiceManager:
    
    eventstore = EventStore()
    dataQueue = queue.Queue()
    webapiFuzzer: webapiFuzzer = None
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServiceManager, cls).__new__(cls)
            
        return cls.instance
    
    
    def delete_api_fuzz_context(self, fuzzcontextId):
        
        try:
            delete_api_fuzz_context(fuzzcontextId)
            
            return (True, '')
            
        except Exception as e:
            return (False, Utils.errAsText(e))
        
        
    
    def update_api_fuzzcontext(self, apiFuzzcontext: ApiFuzzContextUpdate):
        
        try:
            update_api_fuzz_context(apiFuzzcontext)
            
            return (True, '')
        
        except Exception as e:
            ServiceManager.eventstore.emitErr(e)
            return False, Utils.errAsText(e)
        
    
    def new_api_fuzzcontext(self, apiDiscoveryMethod,  
                                name,
                                requestTextContent,
                                requestTextFilePath,
                                openapi3FilePath,
                                openapi3Url,
                                openapi3Content,
                                basicUsername,
                                basicPassword,
                                bearerTokenHeader,
                                bearerToken,
                                apikeyHeader,
                                apikey,
                                hostname,
                                port,
                                fuzzcaseToExec,
                                authnType):
        
        
        isApiDisOK = True
        error = ''
        apicontext= None
        
        try:
            
            if apiDiscoveryMethod == 'openapi3':
                
                if openapi3Content == '':
                    return False, 'OpenApi3 spec content is empty'
                
                openapi3Dis = OpenApi3ApiDiscover()
                
                openapi3Str=  base64.b64decode(openapi3Content).decode('UTF-8')
                
                isApiDisOK, error, apicontext = openapi3Dis.create_apicontext(openapi3Str)
                
                if not isApiDisOK:
                    return False, error
                
                fcc = OpenApi3FuzzContextCreator()
                
                fuzzcontext = fcc.new_fuzzcontext(  apiDiscoveryMethod=apiDiscoveryMethod,
                                                    apicontext=apicontext,
                                                    name=name,
                                                    hostname=hostname,
                                                    port=port,
                                                    requestTextContent = requestTextContent,
                                                    requestTextFilePath = requestTextFilePath,
                                                    openapi3FilePath = openapi3FilePath,
                                                    openapi3Url = openapi3Url,
                                                    openapi3Content = openapi3Content,
                                                    fuzzcaseToExec=fuzzcaseToExec,
                                                    authnType=authnType,
                                                    basicUsername=basicUsername,
                                                    basicPassword=basicPassword,
                                                    bearerTokenHeader=bearerTokenHeader,
                                                    bearerToken=bearerToken,
                                                    apikeyHeader=apikeyHeader,
                                                    apikey=apikey)
                
                insert_db_fuzzcontext(fuzzcontext)
                
            elif apiDiscoveryMethod == 'request_message':
                
                if requestTextContent == '':
                    return False, 'Request text content is empty'
                
                rmStr=  base64.b64decode(requestTextContent).decode('UTF-8')
                
                rmFuzzContextCreator = RequestMessageFuzzContextCreator()
                
                ok, error, fuzzcontext = rmFuzzContextCreator.new_fuzzcontext(apiDiscoveryMethod=apiDiscoveryMethod,
                                                    name=name,
                                                    hostname=hostname,
                                                    port=port,
                                                    requestTextContent = rmStr,
                                                    requestTextFilePath = requestTextFilePath,
                                                    openapi3FilePath = openapi3FilePath,
                                                    openapi3Url = openapi3Url,
                                                    openapi3Content = openapi3Content,
                                                    fuzzcaseToExec=fuzzcaseToExec,
                                                    authnType=authnType,
                                                    basicUsername=basicUsername,
                                                    basicPassword=basicPassword,
                                                    bearerTokenHeader=bearerTokenHeader,
                                                    bearerToken=bearerToken,
                                                    apikeyHeader=apikeyHeader,
                                                    apikey=apikey)
                if not ok:
                    return False, error
                
                insert_db_fuzzcontext(fuzzcontext)
            
            
            return True, ''
            
        except Exception as e:
            self.eventstore.emitErr(e, 'servicemanager.new_api_fuzzcontext')
            return (False, Utils.errAsText(e))
        
        
    
    def save_caseset_selected(self, caseSetSelected):
        
        if caseSetSelected is None or len(caseSetSelected) == 0:
            return (True, '')
        
        try:
            return save_caseset_selected(caseSetSelected)
        except Exception as e:
            return (False, Utils.errAsText(e))
    
    # used internally when fuzzing occurs to get fuzzcontext to fuzz
    def get_fuzzcontext(self, Id) -> ApiFuzzContext:
        try:
            return get_fuzzcontext(Id)
        except Exception as e:
            return (False, Utils.errAsText(e))
        
    
    def get_caseSets_with_runSummary(self, fuzzcontextId, fuzzCaseSetRunId):
        
        try:
            fcsSumRows = get_caseSets_with_runSummary(fuzzcontextId, fuzzCaseSetRunId)
        
            result = []
        
            for row in fcsSumRows:
                
                rowDict = row._asdict()
                
                fcsSum = ApiFuzzCaseSets_With_RunSummary_ViewModel()
            
                fcsSum.fuzzCaseSetId = rowDict['fuzzCaseSetId']                    
                fcsSum.fuzzcontextId = rowDict['fuzzcontextId']
                fcsSum.selected = rowDict['selected']
                fcsSum.verb = rowDict['verb']
                fcsSum.path = rowDict['path']
                fcsSum.querystringNonTemplate = rowDict['querystringNonTemplate']
                fcsSum.bodyNonTemplate = rowDict['bodyNonTemplate']
                fcsSum.headerNonTemplate = rowDict['headerNonTemplate']
                fcsSum.file = rowDict['file']
                
                if 'fuzzCaseSetRunId' in rowDict:
                    fcsSum.fuzzCaseSetRunId = rowDict['fuzzCaseSetRunId']
                else:
                    fcsSum.fuzzCaseSetRunId = ''
                    
                if 'runSummaryId' in rowDict:
                    summaryId = rowDict['runSummaryId']
                    fcsSum.runSummaryId = summaryId
                    fcsSum.http2xx = rowDict['http2xx']
                    fcsSum.http3xx = rowDict['http3xx']
                    fcsSum.http4xx = rowDict['http4xx']
                    fcsSum.http5xx = rowDict['http5xx']
                    fcsSum.completedDataCaseRuns = rowDict['completedDataCaseRuns']
                    fcsSum.totalDataCaseRunsToComplete = rowDict['totalDataCaseRunsToComplete']
                
                result.append(fcsSum)
            
            return (True, '', result)
                
        except Exception as e:
            return (False, Utils.errAsText(e), [])
        
            
    def get_fuzz_request_response(self, fuzzCaseSetId, fuzzCaseSetRunId) -> tuple[bool, str, list[FuzzDataCase_ViewModel]]:
        
        try:
            rows = get_fuzz_request_response(fuzzCaseSetId, fuzzCaseSetRunId)
            
            if rows is None or len(rows) == 0:
                return True, '', []
            
            result = []
            
            for row in rows:
                
                rowDict = row._asdict()
                
                fdc = FuzzDataCase_ViewModel()
                fdc.fuzzDataCaseId = rowDict['fuzzDataCaseId']
                fdc.fuzzCaseSetId = fuzzCaseSetId
                
                fdc.request = FuzzRequest_ViewModel()
                fdc.request.Id = row['fuzzRequestId']
                fdc.request.datetime = row['requestDateTime']
                fdc.request.hostname
                fdc.request.port = rowDict['port']
                fdc.request.verb = rowDict['verb']
                fdc.request.path = rowDict['path']
                fdc.request.querystring = rowDict['querystring']
                fdc.request.url = rowDict['url']
                fdc.request.headers = rowDict['headers']
                #fdc.request.body = rowDict['body']
                fdc.request.contentLength = rowDict['contentLength']
                fdc.request.invalidRequestError = rowDict['invalidRequestError']
                
                fdc.response = FuzzResponse_ViewModel()
                fdc.response.Id = rowDict['fuzzResponseId']
                fdc.response.datetime = row['responseDateTime']
                fdc.response.statusCode = rowDict['statusCode']
                fdc.response.reasonPharse = rowDict['reasonPharse']
                fdc.response.setcookieHeader = rowDict['setcookieHeader']
                fdc.response.headerJson = rowDict['headerJson']
                #fdc.response.body = rowDict['body']
                fdc.response.contentLength = rowDict['contentLength']
                
                result.append(fdc)

            return True, '', result
            
        except Exception as e:
            return (False, Utils.errAsText(e), [])
    
    def get_fuzz_request_response_messages(self, reqId, respId):
        
        if reqId == '' or respId == '':
            return False, 'request id and response id cannot be empty', {}
        
        rrMsg = FuzzRequestResponseMessage()
        
        reqMsg, respMsg, respBody = get_fuzz_request_response_messages(reqId, respId)
        
        if reqMsg == '' or respMsg == '':
            return True, '', {}
        
        rrMsg.requestMessage = reqMsg
        rrMsg.responseMessage = respMsg
        rrMsg.responseBody = respBody
        
        return True, '', rrMsg
        
        
    def get_fuzzContexts_and_runs(self) -> list[ApiFuzzContext_Runs_ViewModel]:
        try:
            ok, err, fcRuns = get_fuzzContexts_and_runs()
            return (ok, err, fcRuns)
        except Exception as e:
            return (False, Utils.errAsText(e), [])
    
    def cancel_fuzz(self):
        try:
            self.webapiFuzzer.cancel_fuzzing()
            #pub.sendMessage(self.eventstore.CancelFuzzWSTopic, command=self.eventstore.CancelFuzzWSTopic)
            return True
        except Exception as e:
            self.eventstore.emitErr(e)
            return False
        
    
    def fuzz(self, fuzzcontextId):
        
        try:
            fuzzcontext = self.get_fuzzcontext(fuzzcontextId)
        
            if fuzzcontext is None:
                return False, 'Context not found or no FuzzCaseSet is selected'
            
            if ServiceManager.webapiFuzzer is None:
                ServiceManager.webapiFuzzer = WebApiFuzzer(fuzzcontext)
                ServiceManager.webapiFuzzer.fuzz()
                
            elif (ServiceManager.webapiFuzzer.fuzzingStatus == FuzzingStatus.Stop):
                
                ServiceManager.webapiFuzzer = None
                ServiceManager.webapiFuzzer = WebApiFuzzer(fuzzcontext)
                ServiceManager.webapiFuzzer.fuzz()
                
            return True, ''
        
        except Exception as e:
            self.eventstore.emitErr(e)
            
    
    def get_webapi_fuzz_info(self) -> WebApiFuzzerInfo:
        
        info = WebApiFuzzerInfo()
        
        if ServiceManager.webapiFuzzer == None:
            info.isFuzzing = False
            
        elif ServiceManager.webapiFuzzer.fuzzingStatus == FuzzingStatus.Fuzzing:
            info.isFuzzing = True
            info.fuzzContextId = ServiceManager.webapiFuzzer.apifuzzcontext.Id
            info.fuzzCaseSetRunId = ServiceManager.webapiFuzzer.fuzzCaseSetRunId
            
        elif (ServiceManager.webapiFuzzer.fuzzingStatus == FuzzingStatus.Stop): 
            info.isFuzzing = False
        
        return info
    
    
    def get_uploaded_files(self, requestId):
        
        try:
            rows = get_uploaded_files(requestId)
            
            if(len(rows) == 0):
                qr = FuzzRequestFileUploadQueryResult()
                qr.ok = True
                qr.error = ''
                qr.result = []
                return qr
        
            rfuList = []
            
            for r in rows:
                
                rDict = r._asdict()
                
                fu =  FuzzRequestFileUpload_ViewModel()
                fu.Id = rDict['Id']
                fu.fileName = rDict['fileName']
                
                rfuList.append(fu)
                
            qr = FuzzRequestFileUploadQueryResult()
            qr.ok = True
            qr.error = ''
            qr.result = rfuList
            return qr
        
        except Exception as e:
            self.eventstore.emitErr(e)
            qr = FuzzRequestFileUploadQueryResult()
            qr.ok = False
            qr.error = Utils.errAsText(e)
            qr.result = []
            return qr
        
    
    def get_uploaded_file_content(self, fileUploadId):
        
        try:
            row = get_uploaded_file_content(fileUploadId)
        
            if row is None:
                r = FuzzRequestFileDownloadContentQueryResult()
                r.ok = True
                r.error = ''
                r.result = ''
                return r
            
            rDict = row._asdict()
            
            r = FuzzRequestFileDownloadContentQueryResult()
            r.ok = True
            r.error = ''
            r.result = rDict['fileContent']
            
            return r
        except Exception as e:
            self.eventstore.emitErr(e)
            r = FuzzRequestFileDownloadContentQueryResult()
            r.ok = False
            r.error = Utils.errAsText(e)
            r.result = ''
            return r
        

    
    
    
    
        

    