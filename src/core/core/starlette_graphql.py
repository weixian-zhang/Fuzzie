import graphene
from datetime import datetime
from pubsub import pub
from servicemanager import ServiceManager
from eventstore import EventStore
from rx import Observable
from graphql_models import ( ApiFuzzCaseSetUpdate, 
                            FuzzContextRunQueryResult, 
                            FuzzRequestResponseQueryResult, 
                            ApiFuzzContextUpdate,
                            FuzzCaseSetRunSummaryQueryResult,
                            FuzzerStatus)
from utils import Utils 

es = EventStore()

# queries
class Query(graphene.ObjectType):
    
    corporaLoaded = False
    corporaLoadMsg = ''
    isFuzzing = False
    
    def on_event_received(command, msgData):
        match command:
            case 'corpora_loaded':
                Query.corporaLoaded = True
            case 'corpora_load_error':
                Query.corporaLoaded = False
                Query.corporaLoadMsg = msgData
            case 'fuzzing_start':
                Query.isFuzzing = True
                Query.corporaLoadMsg = msgData
            case 'fuzzing_stop':
                Query.isFuzzing = False
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
                                         fuzzCaseSetRunId = graphene.Argument(graphene.String))
    
    
    def resolve_fuzzerStatus(self, info):
        
        s = FuzzerStatus()
        
        s.timestamp = Utils.datetimeNowStr()
        s.alive = True
        s.isDataLoaded = Query.corporaLoaded
        s.isFuzzing = Query.isFuzzing
        s.message = Query.corporaLoadMsg
        
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
    
    
    def resolve_fuzzRequestResponse(self, info, fuzzCaseSetId, fuzzCaseSetRunId):
        sm = ServiceManager()
        
        ok , err, result = sm.get_fuzz_request_response(fuzzCaseSetId, fuzzCaseSetRunId)
        
        r = FuzzRequestResponseQueryResult()
          
        r.ok = ok
        r.error = err
        r.result = result
          
        return r
        

class SaveEditedFuzzCaseSets(graphene.Mutation):
    class Arguments:
        fcsus = graphene.List(ApiFuzzCaseSetUpdate)

    #define output
    ok = graphene.Boolean()
    error = graphene.String()
    
    def mutate(self, info, fcsus):
        
        if fcsus is None or len(fcsus) == 0:
            ok = True
            error = ''
            return SaveEditedFuzzCaseSets(ok=ok,error=error) 
        
        sm = ServiceManager()
        
        OK, error = sm.save_caseset_selected(fcsus)

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
               apiDiscoveryMethod,
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
        
        sm = ServiceManager()
        
        OK, error = sm.new_api_fuzzcontext(
                                        apiDiscoveryMethod=apiDiscoveryMethod,
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
        
        
        ok = OK
        error = error
        
        return NewApiFuzzContext(ok=ok,error=error)
    
    
class Fuzz(graphene.Mutation):
    class Arguments:
        fuzzcontextId = graphene.String()


    #define output
    ok = graphene.Boolean()
    msg = graphene.String()
    
    def mutate(self, info, fuzzcontextId):
        
        ok = True
        msg = ''
        
        sm = ServiceManager()
        
        ok, msg = sm.fuzz(fuzzcontextId) #, basicUsername, basicPassword, bearerTokenHeader, bearerToken, apikeyHeader, apikey)

        return Fuzz(ok=ok, msg=msg)
    
class Mutation(graphene.ObjectType):
    
    new_api_fuzz_context = NewApiFuzzContext.Field()
    
    update_api_fuzz_context = UpdateApiContext.Field()
    
    save_api_fuzzcaseset_selected = SaveEditedFuzzCaseSets.Field()
    
    delete_api_fuzz_context = DeleteApiContext.Field()
    
    fuzz = Fuzz.Field()
    
    
schema = graphene.Schema(query=Query, mutation=Mutation) #, subscription= Subscription)

