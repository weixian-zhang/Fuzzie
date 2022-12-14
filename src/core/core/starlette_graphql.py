import graphene
from datetime import datetime
from pubsub import pub
from servicemanager import ServiceManager
from eventstore import EventStore
from rx import Observable
from graphql_models import (ApiFuzzCaseSetUpdate, 
                            FuzzContextRunQueryResult, 
                            ApiFuzzCaseSets_With_RunSummary_ViewModel, 
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
                                              fuzzCaseSetId = graphene.Argument(graphene.String),
                                              fuzzCaseSetRunId = graphene.Argument(graphene.String)
                                              )
    
    
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
    
    def resolve_fuzzCaseSetWithRunSummary(self, info, fuzzcontextId):
        sm = ServiceManager()
        ok, err, result = sm.get_caseSets_with_runSummary(fuzzcontextId)
        
        r = FuzzCaseSetRunSummaryQueryResult(ok, err, result)
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
        # basicUsername = graphene.String()
        # basicPassword = graphene.String()
        # bearerTokenHeader = graphene.String()
        # bearerToken = graphene.String()
        # apikeyHeader = graphene.String()
        # apikey = graphene.String()
        # openapi3Url = graphene.String()

    #define output
    ok = graphene.Boolean()
    msg = graphene.String()
    
    def mutate(self, info, fuzzcontextId):
                    #  basicUsername = '',
                    # basicPassword = '',
                    # bearerTokenHeader = '',
                    # bearerToken = '',
                    # apikeyHeader = '',
                    # apikey = ''):
        
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




# class DiscoverOpenApi3ByUrl(graphene.Mutation):
    
#     class Arguments:
#         name = graphene.String()
#         hostname = graphene.String()
#         port = graphene.Int()
#         authnType = graphene.String()
#         openapi3Url = graphene.String()
    
#     ok = graphene.Boolean()
#     apiFuzzContext = graphene.Field(ApiFuzzContext_Runs_ViewModel)

   
#     def mutate(self, info, hostname, port, openapi3Url, name = '', fuzzmode = 'Quick', numberOfFuzzcaseToExec=50, authnType='Anonymous'):
        
#         sm = ServiceManager()
        
#         fcView = sm.discover_openapi3_by_filepath_or_url(
#                             hostname=hostname,
#                             port=port,
#                             name=name,
#                             fuzzMode= fuzzmode,
#                             numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
#                             authnType=authnType,
#                             openapi3Url=openapi3Url)
        
#         ok = True
#         apiFuzzContext = fcView
        
#         return DiscoverOpenApi3ByUrl(apiFuzzContext=apiFuzzContext, ok=ok)

# import sys, os
# from pathlib import Path
# projectDirPath = os.path.dirname(Path(__file__))
# sys.path.insert(0, os.path.join(projectDirPath, 'models'))
# from apicontext import SupportedAuthnType, ApiVerb
# from fuzzcontext import FuzzProgressState 

# class FuzzMode(graphene.Enum):
#     Quick = 'quick'
#     Full = 'full'
#     Custom = 'custom'
    
# class FuzzProgressState(graphene.Enum):
#     NOTSTARTED = "not started"
#     FUZZING = "still fuzzing"
#     SUCCESS = "success"
#     FAILED = "failed"
    
# class SupportedAuthnType(graphene.Enum):
#     Anonymous = "Anonymous",
#     Basic = "Basic",
#     Bearer = "Bearer",
#     ApiKey = "ApiKey"
    
# class ApiVerb(graphene.Enum):
#     GET = "GET"
#     POST = "POST"
#     PUT = "PUT"
#     PATCH = "PATCH"
#     DELETE = 'DELETE'
    
    
# class ParameterType(graphene.Enum):
#     Path = 'path'
#     Query = 'query'
#     Header = 'header'

# class SecuritySchemes(graphene.ObjectType):
#     authnType = graphene.Field(SupportedAuthnType)
#     basiccUsername = graphene.String()
#     basicPassword = graphene.String()
#     bearerToken = graphene.String()
#     apikeyHeader = graphene.String()
#     apikey = graphene.String()
        
# class ApiFuzzRequest(graphene.ObjectType):
#     Id = graphene.String()
#     datetime = graphene.DateTime()
#     fuzzDataCaseId = graphene.String()
#     fuzzcontextId = graphene.String()
#     hostnamePort = graphene.String()
#     verb= graphene.String()
#     path = graphene.String()
#     querystring= graphene.String()
#     url= graphene.Scalar
#     headers = graphene.List(graphene.String)
#     body = graphene.String()

# class ApiFuzzResponse(graphene.ObjectType):
#     Id = graphene.String()
#     datetime = graphene.DateTime()
#     fuzzDataCaseId = graphene.String()
#     httpVersion = graphene.String()
#     statusCode = graphene.String()
#     headers = graphene.List(graphene.String)
#     body = graphene.String()
#     error = graphene.String()
        

# # each "fuzz data set" is one ApiFuzzCase
# class ApiFuzzDataCase(graphene.ObjectType):
#    id = graphene.String()
#    fuzzCaseSetId = graphene.String()
#    fuzzcontextId = graphene.String()
#    request = graphene.Field(ApiFuzzRequest)
#    response = graphene.Field(ApiFuzzResponse)
#    state = graphene.Field(FuzzProgressState)
        
    
# class ApiFuzzCaseSet(graphene.ObjectType):
#     Id = graphene.String()
#     selected = graphene.Boolean()
#     verb = graphene.Field(ApiVerb) 
#     path = graphene.String()
#     querystringNonTemplate = graphene.String()
#     bodyNonTemplate = graphene.String()
#     headerNonTemplate = graphene.String()
#     authnType = graphene.Field(SupportedAuthnType)
        
        
# class ApiFuzzContext(graphene.ObjectType):
#     Id = graphene.String()
#     name = graphene.String()
#     datetime = graphene.DateTime()
    
#     hostname = graphene.String()
#     port = graphene.Int()
#     fuzzMode = graphene.String()
#     fuzzcaseToExec = graphene.Int(default_value=50)
    
#     requestMessageText = graphene.String()
#     requestMessageFilePath = graphene.String()
#     openapi3FilePath = graphene.String()
#     openapi3Url = graphene.String()
    
#     #security schemes
#     authnType = graphene.Field(SupportedAuthnType)
#     basicUsername = graphene.String()
#     basicPassword  = graphene.String()
#     bearerToken  = graphene.String()
#     apikeyHeader  = graphene.String()
#     apikey  = graphene.String()  
#     fuzzcaseSets = graphene.List(ApiFuzzCaseSet)

