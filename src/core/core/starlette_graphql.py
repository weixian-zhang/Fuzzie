import graphene
from datetime import datetime
from pubsub import pub
from servicemanager import ServiceManager
from eventstore import EventStore
from graphql_models import ( ApiFuzzCaseSetUpdate, 
                            FuzzContextRunQueryResult, 
                            FuzzRequestResponseQueryResult, 
                            ApiFuzzContextUpdate,
                            FuzzCaseSetRunSummaryQueryResult,
                            FuzzerStatus,
                            FuzzRequestResponseMessage_QueryResult,
                            FuzzReqRespMessageQueryResult,
                            FuzzRequestFileUploadQueryResult,
                            FuzzRequestFileDownloadContentQueryResult,
                            ParseRequestMessageResult,
                            FuzzOnceResult
                            )
from utils import Utils 
import base64
import json

es = EventStore()

# queries
class Query(graphene.ObjectType):
    
    corporaLoaded = False
    corporaLoadMsg = ''
    
    #subscribe status event from corpora_loader runnning in background
    def on_event_received(command, msgData):
        match command:
            case 'corpora_loaded':
                Query.corporaLoaded = True
            case 'corpora_load_error':
                Query.corporaLoaded = False
                Query.corporaLoadMsg = msgData
        
                
    pub.subscribe(on_event_received, es.CorporaEventTopic)
    
    fuzzerStatus = graphene.Field(FuzzerStatus)
    
    fuzzContexts = graphene.Field(FuzzContextRunQueryResult)
    
    fuzzCaseSetWithRunSummary = graphene.Field(FuzzCaseSetRunSummaryQueryResult,
                                              fuzzcontextId = graphene.Argument(graphene.String),
                                              fuzzCaseSetRunId = graphene.Argument(graphene.String)
                                              )
    
    fuzzRequestResponse = graphene.Field(FuzzRequestResponseQueryResult,
                                         fuzzCaseSetId = graphene.Argument(graphene.String),
                                         fuzzCaseSetRunId = graphene.Argument(graphene.String),
                                         statusCode=graphene.Argument(graphene.Int), 
                                         pageSize=graphene.Argument(graphene.Int), 
                                         page=graphene.Argument(graphene.Int)
                                         )
    
    
    fuzzRequestResponseMessage = graphene.Field(FuzzRequestResponseMessage_QueryResult,
                                                reqId = graphene.Argument(graphene.String),
                                                respId = graphene.Argument(graphene.String))
    
    parseRequestMessageResult = graphene.Field(ParseRequestMessageResult, rqMsg = graphene.Argument(graphene.String))
    
    
    getUploadedFiles = graphene.Field(FuzzRequestFileUploadQueryResult, requestId = graphene.Argument(graphene.String))
    
    downloadFuzzFile = graphene.Field(FuzzRequestFileDownloadContentQueryResult, fuzzFileUploadId = graphene.Argument(graphene.String))
    
    searchBody = graphene.Field(FuzzRequestResponseQueryResult,
                                         searchText = graphene.Argument(graphene.String),
                                         fuzzCaseSetId = graphene.Argument(graphene.String),
                                         fuzzCaseSetRunId = graphene.Argument(graphene.String))
    
    def resolve_fuzzerStatus(self, info):
        
        s = FuzzerStatus()
        
        sm = ServiceManager()
        
        s.timestamp = Utils.datetimeNowStr()
        s.alive = True
        s.isDataLoaded = Query.corporaLoaded
        s.message = Query.corporaLoadMsg
        s.webapiFuzzerInfo = sm.get_webapi_fuzz_info()
        
        return s
    
    
    def resolve_fuzzContexts(self, info):
        sm = ServiceManager()
        ok, err, result = sm.get_fuzzContexts_and_runs()
        
        r = FuzzContextRunQueryResult()
        r.ok = ok
        r.error = err
        r.result = result
        return r       
    
    def resolve_fuzzCaseSetWithRunSummary(self, info, fuzzcontextId, fuzzCaseSetRunId):
        sm = ServiceManager()
        ok, err, result = sm.get_caseSets_with_runSummary(fuzzcontextId, fuzzCaseSetRunId)
        
        r = FuzzCaseSetRunSummaryQueryResult()
        r.ok = ok
        r.error = err
        r.result = result
          
        return r
    
    
    def resolve_fuzzRequestResponse(self, info, fuzzCaseSetId, fuzzCaseSetRunId, statusCode = -1, pageSize=500, page=1):
        sm = ServiceManager()
        
        ok , err, totalPages, result = sm.get_fuzz_request_response(fuzzCaseSetId, fuzzCaseSetRunId, statusCode, pageSize, page)
        
        r = FuzzRequestResponseQueryResult()
          
        r.ok = ok
        r.error = err
        r.totalPages = totalPages
        r.result = result
          
        return r
    
    def resolve_fuzzRequestResponseMessage(self, info, reqId, respId):
        
        sm = ServiceManager()
        
        ok, error, result = sm.get_fuzz_request_response_messages(reqId, respId)
        
        r = FuzzRequestResponseMessage_QueryResult()
        r.ok = ok
        r.error = error
        r.result = result
        
        return r
    
    def resolve_searchBody(self, info, searchText, fuzzCaseSetId, fuzzCaseSetRunId):
        
        sm = ServiceManager()
        
        ok , err, result = sm.search_body(searchText, fuzzCaseSetId, fuzzCaseSetRunId)
        
        r = FuzzRequestResponseQueryResult()
          
        r.ok = ok
        r.error = err
        r.result = result
          
        return r
    
    def resolve_getUploadedFiles(self, info, requestId):
        
        sm = ServiceManager()
        
        result = sm.get_uploaded_files(requestId)
        
        return result
    
    def resolve_downloadFuzzFile(self, info, fuzzFileUploadId):
        
        sm = ServiceManager()
        
        ok, error, content = sm.get_uploaded_file_content(fuzzFileUploadId)
        
        r = FuzzRequestFileDownloadContentQueryResult()
        r.ok = True
        r.error = ''
        r.result = content
        
        return r
    
    def resolve_parseRequestMessageResult(self, info, rqMsg):
        
        sm = ServiceManager()
        
        ok, error = sm.parse_request_message(rqMsg)
        
        r = ParseRequestMessageResult()
        r.ok = ok
        r.error = error
        
        return r
        
        

class SaveEditedFuzzCaseSets(graphene.Mutation):
    class Arguments:
        fuzzcontextId = graphene.String()
        fcsus = graphene.String() #graphene.List(ApiFuzzCaseSetUpdate)

    #define output
    ok = graphene.Boolean()
    error = graphene.String()
    
    def mutate(self, info, fuzzcontextId, fcsus):
        if fcsus == '':
            return True, ''
        
        b64d = base64.b64decode(fcsus)
        
        fcsList = json.loads(b64d)
        
        if fcsList is None or len(fcsList) == 0:
            ok = True
            error = ''
            return SaveEditedFuzzCaseSets(ok=ok,error=error) 
        
        sm = ServiceManager()
        
        OK, error = sm.save_updated_fuzzcasesets(fuzzcontextId, fcsList)

        ok = OK
        error = error
        
        return SaveEditedFuzzCaseSets(ok=ok,error=error)

class DeleteApiContext(graphene.Mutation):
    class Arguments:
        fuzzcontextId= graphene.String()

    #define output
    ok = graphene.Boolean()
    error = graphene.String()
    
    def mutate(self, info, fuzzcontextId):
        
        if Utils.isNoneEmpty(fuzzcontextId):
            ok = False
            error = 'fuzz context id cannot be empty when deleting a fuzz context'
            return DeleteApiContext(ok=ok,error=error) 
        
        sm = ServiceManager()
        
        OK, error = sm.delete_api_fuzz_context(fuzzcontextId)

        ok = OK
        error = error
        
        return DeleteApiContext(ok=ok,error=error)

class DeleteApiFuzzCaseSetRun(graphene.Mutation):
    class Arguments:
        fuzzCaseSetRunId= graphene.String()

    #define output
    ok = graphene.Boolean()
    error = graphene.String()
    
    def mutate(self, info, fuzzCaseSetRunId):
        
        if Utils.isNoneEmpty(fuzzCaseSetRunId):
            ok = False
            error = 'fuzz-run-id cannot be empty when deleting a fuzz-run'
            return DeleteApiFuzzCaseSetRun(ok=ok,error=error) 
        
        sm = ServiceManager()
        
        OK, error = sm.delete_api_fuzzCaseSetRun(fuzzCaseSetRunId)

        ok = OK
        error = error
        
        return DeleteApiFuzzCaseSetRun(ok=ok,error=error)

class UpdateApiContext(graphene.Mutation):
    class Arguments:
        fuzzContext= ApiFuzzContextUpdate(required=True)

    #define output
    ok = graphene.Boolean()
    error = graphene.String()
    
    def mutate(self, info, fuzzContext):
        
        sm = ServiceManager()
        
        OK, error = sm.update_api_fuzzcontext(fuzzContext)

        ok = OK
        error = error
        
        return UpdateApiContext(ok=ok,error=error)
    
class NewApiFuzzContext(graphene.Mutation):
    
    class Arguments:
        apiDiscoveryMethod = graphene.String()
        name = graphene.String()
        requestTextContent = graphene.String()
        requestTextFilePath = graphene.String()
        openapi3FilePath = graphene.String()
        openapi3Url = graphene.String()
        openapi3Content = graphene.String()
        basicUsername = graphene.String() 
        basicPassword = graphene.String() 
        bearerTokenHeader = graphene.String() 
        bearerToken = graphene.String() 
        apikeyHeader = graphene.String() 
        apikey = graphene.String() 
        hostname = graphene.String()
        port = graphene.Int()
        fuzzcaseToExec = graphene.Int()
        authnType = graphene.String()
    
    ok = graphene.Boolean()
    error = graphene.String()
    
    def mutate(self, info,
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
                fuzzcaseToExec,
                authnType):
        
        sm = ServiceManager()
        
        OK, error = sm.new_api_fuzzcontext(
                                        name=name,
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
        
        
        ok = OK
        error = error
        
        return NewApiFuzzContext(ok=ok,error=error)

class CancelFuzz(graphene.Mutation):
    
    #define output
    ok = graphene.Boolean()
    
    def mutate(self, info):
        
        ok = True
        
        sm = ServiceManager()
        sm.cancel_fuzz()
        
        return CancelFuzz(ok)

class FuzzOnce(graphene.Mutation):
    class Arguments:
        fuzzcontextId = graphene.String()
        fuzzCaseSetId = graphene.String()

    #define output
    ok = graphene.Boolean()
    msg = graphene.String()
    caseSetRunSummaryId = graphene.String()
    
    def mutate(self, info, fuzzcontextId, fuzzCaseSetId):
        
        ok = True
        msg = ''
        
        sm = ServiceManager()
        
        ok, msg, caseSetRunSummaryId = sm.fuzz_once(fuzzcontextId, fuzzCaseSetId) #, basicUsername, basicPassword, bearerTokenHeader, bearerToken, apikeyHeader, apikey)

        return FuzzOnce(ok=ok, msg=msg, caseSetRunSummaryId=caseSetRunSummaryId)
    
class Fuzz(graphene.Mutation):
    class Arguments:
        fuzzcontextId = graphene.String()

    #define output
    ok = graphene.Boolean()
    msg = graphene.String()
    
    async def mutate(self, info, fuzzcontextId):
        
        ok = True
        msg = ''
        
        sm = ServiceManager()
        
        ok, msg = await sm.fuzz(fuzzcontextId) #, basicUsername, basicPassword, bearerTokenHeader, bearerToken, apikeyHeader, apikey)

        return Fuzz(ok=ok, msg=msg)
    
class Mutation(graphene.ObjectType):
    
    new_api_fuzz_context = NewApiFuzzContext.Field()
    
    update_api_fuzz_context = UpdateApiContext.Field()
    
    save_api_fuzzcaseset= SaveEditedFuzzCaseSets.Field()
    
    delete_api_fuzz_context = DeleteApiContext.Field()
    
    delete_api_fuzzcasesetrun =  DeleteApiFuzzCaseSetRun.Field()
    
    fuzz = Fuzz.Field()
    
    fuzz_once = FuzzOnce.Field()
    
    cancel_Fuzz = CancelFuzz.Field()
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)

