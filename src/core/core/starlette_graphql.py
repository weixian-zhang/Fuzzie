import graphene
import asyncio
from servicemanager import ServiceManager
from eventstore import EventStore
from datetime import datetime
from rx import Observable
from graphql_models import ApiFuzzContext_Runs_ViewModel, ApiFuzzCaseSets_With_RunSummary_ViewModel

# queries
class Query(graphene.ObjectType):
    
    alive = graphene.String()
    
    fuzzContexts = graphene.List(ApiFuzzContext_Runs_ViewModel)
    
    fuzzCaseSetWithRunSummary = graphene.List(ApiFuzzCaseSets_With_RunSummary_ViewModel,
                                              fuzzcontextId = graphene.Argument(graphene.String))
    
    
    def resolve_alive(self, info):
        return "alive"
    
    
    def resolve_fuzzContexts(self, info):
        sm = ServiceManager()
        result = sm.get_fuzzContexts()
        return result
    
    def resolve_fuzzCaseSetWithRunSummary(self, info, fuzzcontextId):
        sm = ServiceManager()
        result = sm.get_caseSets_with_runSummary(fuzzcontextId)
        return result
    

    
class NewFuzzContext(graphene.Mutation):
    
    class Arguments:
        isanonymous = graphene.Boolean
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
    apiFuzzContext = graphene.Field(ApiFuzzContext_Runs_ViewModel)
    
    def mutate(self, info,
               isanonymous,
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
        
        fuzzcontext = sm.discover_openapi3_by_filepath_or_url(
                            hostname=hostname,
                            port=port,
                            name=name,
                            fuzzMode= fuzzmode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            authnType=authnType,
                            openapi3FilePath=openapi3FilePath)
        
        ok = True
        apiFuzzContext = fuzzcontext
        
        return DiscoverOpenApi3ByFilePath(apiFuzzContext=apiFuzzContext, ok=ok)
    
class DiscoverOpenApi3ByUrl(graphene.Mutation):
    
    class Arguments:
        name = graphene.String()
        hostname = graphene.String()
        port = graphene.Int()
        authnType = graphene.String()
        openapi3Url = graphene.String()
    
    ok = graphene.Boolean()
    apiFuzzContext = graphene.Field(ApiFuzzContext_Runs_ViewModel)

   
    def mutate(self, info, hostname, port, openapi3Url, name = '', fuzzmode = 'Quick', numberOfFuzzcaseToExec=50, authnType='Anonymous'):
        
        sm = ServiceManager()
        
        fcView = sm.discover_openapi3_by_filepath_or_url(
                            hostname=hostname,
                            port=port,
                            name=name,
                            fuzzMode= fuzzmode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            authnType=authnType,
                            openapi3Url=openapi3Url)
        
        ok = True
        apiFuzzContext = fcView
        
        return DiscoverOpenApi3ByUrl(apiFuzzContext=apiFuzzContext, ok=ok)
    
class Fuzz(graphene.Mutation):
    class Arguments:
        fuzzcontextId = graphene.String()
        basicUsername = graphene.String()
        basicPassword = graphene.String()
        bearerTokenHeader = graphene.String()
        bearerToken = graphene.String()
        apikeyHeader = graphene.String()
        apikey = graphene.String()
        openapi3Url = graphene.String()

    #define output
    ok = graphene.Boolean()
    
    def mutate(self, info, 
                     fuzzcontextId,
                     basicUsername = '',
                    basicPassword = '',
                    bearerTokenHeader = '',
                    bearerToken = '',
                    apikeyHeader = '',
                    apikey = ''):
        
        ok = True
        
        sm = ServiceManager()
        
        sm.fuzz(fuzzcontextId, basicUsername, basicPassword, bearerTokenHeader, bearerToken, apikeyHeader, apikey)

        return Fuzz(ok=ok)
    
class Mutation(graphene.ObjectType):
    
    discover_by_openapi3_file_path = DiscoverOpenApi3ByFilePath.Field()
    
    discover_by_openapi3_url = DiscoverOpenApi3ByUrl.Field()
    
    fuzz = Fuzz.Field()
    
    #discoverBySingleRequestText(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    #discoverByRequestTextFilePath(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    
schema = graphene.Schema(query=Query, mutation=Mutation) #, subscription= Subscription)

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

