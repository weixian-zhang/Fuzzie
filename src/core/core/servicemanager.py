# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext
from graphql_models import (ApiFuzzContext_Runs_ViewModel, 
                            ApiFuzzContextUpdate, 
                            ApiFuzzCaseSets_With_RunSummary_ViewModel,
                            FuzzRequest_ViewModel,
                            FuzzResponse_ViewModel,
                            FuzzDataCase_ViewModel)
from webapi_fuzzer import WebApiFuzzer
from automapper import mapper
from eventstore import EventStore, MsgType
from utils import Utils
from db import  (get_caseSets_with_runSummary,
                 insert_db_fuzzcontext, 
                 update_api_fuzz_context,
                 delete_api_fuzz_context,
                 get_fuzzContexts_and_runs,
                 save_caseset_selected,
                 get_fuzz_request_response)
from sqlalchemy.sql import select, insert
import base64

import threading, time
from datetime import datetime
import queue

def bgWorkerDataToClient():
    
    while True:
        
        try:
            data = ServiceManager.dataQueue.get()
        
            if data != '':
                ServiceManager.eventstore.feedback_client(data, MsgType.FuzzEvent)
                
            time.sleep(1)
        except Exception as e:
            print(e)
        
        
class ServiceManager:
    
    eventstore = EventStore()
    dataQueue = queue.Queue()
    bgWorkerDataToClient = None
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServiceManager, cls).__new__(cls)
            threading.Thread(target=bgWorkerDataToClient, daemon=True).start()
        return cls.instance
    
    def __init__(self) -> None:   
        pass
    
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
        
        openapi3Dis = OpenApi3ApiDiscover()
        isApiDisOK = True
        error = ''
        apicontext= None
        
        rtStr=  base64.b64decode(requestTextContent).decode('UTF-8')
        openapi3Str=  base64.b64decode(openapi3Content).decode('UTF-8')
        
        if apiDiscoveryMethod == 'openapi3':
            
            if openapi3Str == '':
                return False, 'OpenApi3 spec content is empty'
            
            isApiDisOK, error, apicontext = openapi3Dis.create_apicontext_from_openapi3(openapi3Str)
            
        elif apiDiscoveryMethod == 'request-text':
            
            if rtStr == '':
                return False, 'Request text content is empty'
            
            pass
        
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
        
        return True, ''
    
    def save_caseset_selected(self, caseSetSelected):
        
        if caseSetSelected is None or len(caseSetSelected) == 0:
            return (True, '')
        
        try:
            return save_caseset_selected(caseSetSelected)
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
                fdc.request.requestDateTime = row['requestDateTime']
                fdc.request.hostname
                fdc.request.port = rowDict['port']
                fdc.request.verb = rowDict['verb']
                fdc.request.path = rowDict['path']
                fdc.request.querystring = rowDict['querystring']
                fdc.request.url = rowDict['url']
                fdc.request.headers = rowDict['headers']
                fdc.request.body = rowDict['body']
                fdc.request.contentLength = rowDict['contentLength']
                fdc.request.requestMessage = rowDict['requestMessage']
                
                fdc.response = FuzzResponse_ViewModel()
                fdc.response.Id = rowDict['fuzzResponseId']
                fdc.response.responseDateTime = row['responseDateTime']
                fdc.response.statusCode = rowDict['statusCode']
                fdc.response.reasonPharse = rowDict['reasonPharse']
                fdc.response.setcookieHeader = rowDict['setcookieHeader']
                fdc.response.headerJson = rowDict['headerJson']
                fdc.response.body = rowDict['body']
                fdc.response.contentLength = rowDict['contentLength']
                fdc.response.responseDisplayText = rowDict['responseDisplayText']
                
                result.append(fdc)

            return True, '', result
            
        except Exception as e:
            return (False, Utils.errAsText(e), [])
        
        
    def get_fuzzContexts_and_runs(self) -> list[ApiFuzzContext_Runs_ViewModel]:
        try:
            ok, err, fcRuns = get_fuzzContexts_and_runs()
            return (ok, err, fcRuns)
        except Exception as e:
            return (False, Utils.errAsText(e), [])
    

    def fuzz(self, fuzzcontextId):
        
        fuzzcontext = self.get_fuzzcontext(fuzzcontextId)
        
        if fuzzcontext is None:
            return False, 'Context not found or no FuzzCaseSet is selected'
        
        webapifuzzer = WebApiFuzzer(fuzzcontext)
                                    # ServiceManager.dataQueue, 
                                    # basicUsername = basicUsername, 
                                    # basicPassword= basicPassword, 
                                    # bearerTokenHeader= bearerTokenHeader,
                                    # bearerToken= bearerToken, 
                                    # apikeyHeader=  apikeyHeader, 
                                    # apikey= apikey)
        
        webapifuzzer.fuzz()
        
        return True, ''
        
    
    
    
    
        

    