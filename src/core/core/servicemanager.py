# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

# from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
# from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
# from api_discovery.requestmessage_fuzzcontext_creator import RequestMessageFuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext, FuzzCaseSetFile
from graphql_models import (ApiFuzzContext_Runs_ViewModel, 
                            ApiFuzzContextUpdate, 
                            ApiFuzzCaseSets_With_RunSummary_ViewModel,
                            FuzzRequest_ViewModel,
                            FuzzResponse_ViewModel,
                            FuzzDataCase_ViewModel,
                            WebApiFuzzerInfo,
                            FuzzRequestResponseMessage_ViewModel,
                            FuzzRequestFileUpload_ViewModel,
                            FuzzRequestFileUploadQueryResult,
                            FuzzRequestFileDownloadContentQueryResult)
from corporafactory.corpora_context import CorporaContext
from corporafactory.corpora_context_builder import CorporaContextBuilder
from webapi_fuzzer import WebApiFuzzer, FuzzingStatus
from eventstore import EventStore, MsgType
from utils import Utils
from db import  (get_fuzzcontext,
                 get_caseSets_with_runSummary,
                 insert_db_fuzzcontext, 
                 update_api_fuzz_context,
                 delete_api_fuzz_context,
                 delete_api_fuzzCaseSetRun,
                 get_fuzzContexts_and_runs,
                 save_updated_fuzzcasesets,
                 update_rqmsg_in_fuzz_context,
                 update_api_fuzz_context,
                 get_fuzz_request_response,
                 get_fuzz_request_response_messages,
                 get_uploaded_files,
                 get_uploaded_file_content,
                 search_body,
                 get_request_response_total_pages)
from sqlalchemy.sql import select, insert
import base64
from pubsub import pub
from datetime import datetime
import queue
from api_discovery.requestmessage_fuzzcontext_creator import RequestMessageFuzzContextCreator

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
    
    def delete_api_fuzzCaseSetRun(self, fuzzCaseSetRunId):
        
        try:
            delete_api_fuzzCaseSetRun(fuzzCaseSetRunId)
            
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
                
                pass
                # if openapi3Content == '':
                #     return False, 'OpenApi3 spec content is empty'
                
                # openapi3Dis = OpenApi3ApiDiscover()
                
                # openapi3Str=  base64.b64decode(openapi3Content).decode('UTF-8')
                
                # isApiDisOK, error, apicontext = openapi3Dis.create_apicontext(openapi3Str)
                
                # if not isApiDisOK:
                #     return False, error
                
                # fcc = OpenApi3FuzzContextCreator()
                
                # fuzzcontext = fcc.new_fuzzcontext(  apiDiscoveryMethod=apiDiscoveryMethod,
                #                                     apicontext=apicontext,
                #                                     name=name,
                #                                     hostname=hostname,
                #                                     port=port,
                #                                     requestTextContent = requestTextContent,
                #                                     requestTextFilePath = requestTextFilePath,
                #                                     openapi3FilePath = openapi3FilePath,
                #                                     openapi3Url = openapi3Url,
                #                                     openapi3Content = openapi3Content,
                #                                     fuzzcaseToExec=fuzzcaseToExec,
                #                                     authnType=authnType,
                #                                     basicUsername=basicUsername,
                #                                     basicPassword=basicPassword,
                #                                     bearerTokenHeader=bearerTokenHeader,
                #                                     bearerToken=bearerToken,
                #                                     apikeyHeader=apikeyHeader,
                #                                     apikey=apikey)
                
                # insert_db_fuzzcontext(fuzzcontext)
                
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
        
        
    
    def save_updated_fuzzcasesets(self, fuzzcontextId: str, fcsList: list):
        
        if fcsList is None or len(fcsList) == 0:
            return (True, '')
        
        try:
            
            rqParser = RequestMessageFuzzContextCreator()
            
            allUpdatedRqMsgs = []
            parsedFCSs = {}
            
            for unParsedFCS in fcsList:
                
                rq = unParsedFCS['requestMessage']
                
                if rq == '':
                    continue
                
                # parse only first request-msg-block even though at FuzzCaseSet level user may accidentally add more than 1 rq-msg
                ok, err, singleFCS = rqParser.parse_first_request_msg_as_single_fuzzcaseset(rq)
                
                if ok and singleFCS != None:
                    
                    parsedRequestMsg = singleFCS.requestMessage
                    
                    parsedFCSs['fuzzCaseSetId'] = unParsedFCS['fuzzCaseSetId']
                    parsedFCSs['selected'] = unParsedFCS['selected']
                    parsedFCSs['verb'] = singleFCS.verb
                    parsedFCSs['hostname'] =  singleFCS.hostname
                    parsedFCSs['port'] = singleFCS.port
                    parsedFCSs['path'] = singleFCS.path
                    parsedFCSs['querystringNonTemplate'] = singleFCS.querystringNonTemplate
                    parsedFCSs['bodyNonTemplate'] = singleFCS.bodyNonTemplate
                    parsedFCSs['headerNonTemplate'] = singleFCS.headerNonTemplate
                    
                    if singleFCS.file != '':
                        parsedFCSs['file'] = singleFCS.file.wordlist_type
                        parsedFCSs['fileName'] = singleFCS.file.filename
                    else:
                        parsedFCSs['file'] = ''
                        parsedFCSs['fileName'] = ''
                    
                    parsedFCSs['isGraphQL'] = singleFCS.isGraphQL
                    parsedFCSs['graphQLVariableNonTemplate'] = singleFCS.graphQLVariableNonTemplate 
                    parsedFCSs['graphQLVariableDataTemplate'] = singleFCS.graphQLVariableDataTemplate
                    
                    parsedFCSs['fileDataTemplate'] = singleFCS.fileDataTemplate 
                    parsedFCSs['pathDataTemplate'] = singleFCS.pathDataTemplate
                    parsedFCSs['querystringDataTemplate'] = singleFCS.querystringDataTemplate
                    parsedFCSs['bodyDataTemplate'] = singleFCS.bodyDataTemplate
                    parsedFCSs['headerDataTemplate'] = singleFCS.headerDataTemplate
                    parsedFCSs['requestMessage'] = parsedRequestMsg

                    allUpdatedRqMsgs.append(parsedRequestMsg)
            
                    fcsOK, fcsError = save_updated_fuzzcasesets(parsedFCSs)
                    
                    if not fcsOK:
                        self.eventstore.emitErr(fcsError)
            
            # FuzzCaseSet.requestMessage is update, now update the "whole" fuzzcontext.requestTextContent
            if len(allUpdatedRqMsgs) > 0:
                newEntireRqMsg = '\n\n###\n\n'.join(map(str,allUpdatedRqMsgs))
                update_rqmsg_in_fuzz_context(rqMsg=newEntireRqMsg, fuzzcontextId=fuzzcontextId)
                
            return True, ''
                
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
                fcsSum.hostname = rowDict['hostname']
                fcsSum.port = rowDict['port']
                fcsSum.verb = rowDict['verb']
                fcsSum.path = rowDict['path']
                fcsSum.querystringNonTemplate = rowDict['querystringNonTemplate']
                fcsSum.bodyNonTemplate = rowDict['bodyNonTemplate']
                fcsSum.headerNonTemplate = rowDict['headerNonTemplate']
                fcsSum.file = rowDict['file']
                fcsSum.fileName = rowDict['fileName']
                fcsSum.requestMessage = rowDict['requestMessage']
                fcsSum.isGraphQL = rowDict['isGraphQL']
                fcsSum.graphQLVariableNonTemplate = rowDict['graphQLVariableNonTemplate']
                fcsSum.graphQLVariableDataTemplate = rowDict['graphQLVariableDataTemplate']
                fcsSum.totalDataCaseRunsToComplete = rowDict['fuzzcaseToExec']
                
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
        
            
    def get_fuzz_request_response(self, fuzzCaseSetId, fuzzCaseSetRunId, statusCode = -1, pageSize=500, page=1) -> tuple[bool, str, int, list[FuzzDataCase_ViewModel]]:
        
        try:
            rows = get_fuzz_request_response(fuzzCaseSetId, fuzzCaseSetRunId, statusCode, pageSize, page)
            
            if rows is None or len(rows) == 0:
                return True, '', 0, []
            
            result = []
            
            totalPages = get_request_response_total_pages(fuzzCaseSetId=fuzzCaseSetId, fuzzCaseSetRunId=fuzzCaseSetRunId, statusCode=statusCode)
            
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
                # fdc.request.body = rowDict['body']
                fdc.request.contentLength = rowDict['contentLength']
                fdc.request.invalidRequestError = rowDict['invalidRequestError']
                
                fdc.response = FuzzResponse_ViewModel()
                
                fdc.response.Id = rowDict['fuzzResponseId']
                fdc.response.datetime = row['responseDateTime']
                fdc.response.statusCode = rowDict['statusCode']
                fdc.response.reasonPharse = rowDict['reasonPharse']
                fdc.response.setcookieHeader = rowDict['setcookieHeader']
                fdc.response.headerJson = rowDict['headerJson']
                # fdc.response.body = rowDict['body']
                fdc.response.contentLength = rowDict['contentLength']
                
                result.append(fdc)

            return True, '', totalPages, result
            
        except Exception as e:
            return (False, Utils.errAsText(e), [])
    
    def get_fuzz_request_response_messages(self, reqId, respId) -> tuple([bool, str, FuzzRequestResponseMessage_ViewModel]):
        
        if reqId == '' or respId == '':
            return False, 'request id and response id cannot be empty', {}
    
        
        ok, error, reqDict, respDict = get_fuzz_request_response_messages(reqId, respId)
        
        if not ok:
            return True, '', FuzzRequestResponseMessage_ViewModel()
        
        requestMsg = reqDict['requestMessage']
        responseMsg = respDict['responseDisplayText']
        responseBody = respDict['responseBody']
        
        if requestMsg != '':
            requestMsg = base64.b64decode(requestMsg).decode('utf-8')
            
        if responseMsg != '':
            responseMsg = base64.b64decode(responseMsg).decode('utf-8')
            
        if responseBody != '':
            responseBody = base64.b64decode(responseBody).decode('utf-8')
        
        rrMsg = FuzzRequestResponseMessage_ViewModel()
        rrMsg.ok = True
        rrMsg.error = ''
        rrMsg.requestVerb = reqDict['verb']
        rrMsg.requestMessage = requestMsg
        rrMsg.requestPath = reqDict['path']
        rrMsg.requestQuerystring = reqDict['querystring']
        rrMsg.requestHeader = reqDict['headers']
        rrMsg.requestBody = reqDict['body']
        
        rrMsg.responseDisplayText = responseMsg
        rrMsg.responseReasonPhrase = respDict['reasonPharse']
        rrMsg.responseHeader = respDict['headerJson']
        rrMsg.responseBody= responseBody
        
        
        return True, '', rrMsg
    
    
    def search_body(self, searchText: str, fuzzCaseSetId = '', fuzzCaseSetRunId = ''):
             
        try:
            rows = search_body(searchText, fuzzCaseSetId, fuzzCaseSetRunId)
            
            if rows is None or len(rows) == 0:
                return True, '', []
            
            result = []
            
            for row in rows:
                
                rowDict = row._asdict()
                
                reqBody: str = Utils.try_decode_bytes_string(base64.b64decode(rowDict['requestBody']))
                respBody: str = Utils.try_decode_bytes_string(base64.b64decode(rowDict['responseBody']))
                
                searchText = searchText.lower()

                if searchText in reqBody.lower() or searchText in respBody.lower():
                    
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
                    fdc.request.contentLength = rowDict['contentLength']
                    fdc.request.invalidRequestError = rowDict['invalidRequestError']
                    
                    fdc.response = FuzzResponse_ViewModel()
                    
                    fdc.response.Id = rowDict['fuzzResponseId']
                    fdc.response.datetime = row['responseDateTime']
                    fdc.response.statusCode = rowDict['statusCode']
                    fdc.response.reasonPharse = rowDict['reasonPharse']
                    fdc.response.setcookieHeader = rowDict['setcookieHeader']
                    fdc.response.headerJson = rowDict['headerJson']
                    fdc.response.contentLength = rowDict['contentLength']
                    
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
    
    def cancel_fuzz(self):
        try:
            if ServiceManager.webapiFuzzer is not None:
                ServiceManager.webapiFuzzer.cancel_fuzzing()
                ServiceManager.webapiFuzzer = None
                return True
        except Exception as e:
            self.eventstore.emitErr(e, 'ServiceManager.cancel_fuzz')
            return False
    
    def fuzz_once(self, fuzzcontextId, fuzzcasesetId) -> tuple([bool, str, str]):
        try:
            fuzzcontext = self.get_fuzzcontext(fuzzcontextId)
            
            # find single fuzzcaseset
            singleFCSList = []
            for x in fuzzcontext.fuzzcaseSets:
                if x.Id == fuzzcasesetId:
                    singleFCSList.append(x)
                    break
                
            fuzzcontext.fuzzcaseSets = singleFCSList
        
            if fuzzcontext is None:
                return False, 'Context not found or no FuzzCaseSet is selected'
            
            if ServiceManager.webapiFuzzer is None or ServiceManager.webapiFuzzer.fuzzingStatus == FuzzingStatus.Stop:
                ServiceManager.webapiFuzzer = WebApiFuzzer(fuzzcontext)
                caseSetRunSummaryId = ServiceManager.webapiFuzzer.fuzz_once(fuzzcasesetId)
            else:
                return False, 'fuzzing in progress'
                
            return True, '', caseSetRunSummaryId
        
        except Exception as e:
            self.eventstore.emitErr(e)
    
    async def fuzz(self, fuzzcontextId):
        
        try:
            fuzzcontext = self.get_fuzzcontext(fuzzcontextId)
        
            if fuzzcontext is None:
                return False, 'Context not found or no FuzzCaseSet is selected'
            
            if ServiceManager.webapiFuzzer is None or ServiceManager.webapiFuzzer.fuzzingStatus == FuzzingStatus.Stop:
                ServiceManager.webapiFuzzer = WebApiFuzzer(fuzzcontext)
                await ServiceManager.webapiFuzzer.fuzz()
            else:
                return False, 'fuzzing in progress'
            
            return True, ''
        
        except Exception as e:
            ServiceManager.webapiFuzzer = None
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
                return True, '', ''
            
            rDict = row._asdict()
            
            fileContent = rDict['fileContent']
            
            #b64Encoded = base64.b64encode(bytes(byteContent, 'utf-8'))
            
            return True, '', fileContent
        
        except Exception as e:
            self.eventstore.emitErr(e)
            r = FuzzRequestFileDownloadContentQueryResult()
            r.ok = False
            r.error = Utils.errAsText(e)
            r.result = ''
            return r
        
        
    def parse_request_message(self, rqMsgB64: str) -> tuple([bool, str]):
        
        try:
            
            rqMsg = base64.b64decode(rqMsgB64).decode('utf-8')
            
            reqMsgFuzzCaseSetCreator = RequestMessageFuzzContextCreator()
            
            fcsOK, fcsErr, fuzzCaseSets = reqMsgFuzzCaseSetCreator.parse_request_msg_as_fuzzcasesets(rqMsg)
            
            if not fcsOK:
                return False, fcsErr
            
            cp = CorporaContext()
            ccBuilder = CorporaContextBuilder(cp)
            
            ok, error = ccBuilder.build_for_api(fuzzCaseSets, tryBuild=True)
            
            #ok, error = cp.try_build_context(fuzzCaseSets)
            
            if not ok:
                return False, error
            
            reqMsgFuzzCaseSetCreator = None
            cp = None
            
            return ok, error
        
        except Exception as e:
            self.eventstore.emitErr(e)
            return False, Utils.errAsText(e)
            
        
        

    
    
    
    
        

    