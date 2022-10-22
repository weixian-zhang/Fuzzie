import graphene
import asyncio
from servicemanager import ServiceManager
from eventstore import EventStore
from datetime import datetime
from rx import Observable

# import sys, os
# from pathlib import Path
# projectDirPath = os.path.dirname(Path(__file__))
# sys.path.insert(0, os.path.join(projectDirPath, 'models'))
# from apicontext import SupportedAuthnType, ApiVerb
# from fuzzcontext import FuzzProgressState 

class FuzzMode(graphene.Enum):
    Quick = 'quick'
    Full = 'full'
    Custom = 'custom'
    
class FuzzProgressState(graphene.Enum):
    NOTSTARTED = "not started"
    FUZZING = "still fuzzing"
    SUCCESS = "success"
    FAILED = "failed"
    
class SupportedAuthnType(graphene.Enum):
    Anonymous = "Anonymous",
    Basic = "Basic",
    Bearer = "Bearer",
    ApiKey = "ApiKey"
    
class ApiVerb(graphene.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = 'DELETE'
    
    
class ParameterType(graphene.Enum):
    Path = 'path'
    Query = 'query'
    Header = 'header'

class SecuritySchemes(graphene.ObjectType):
    authnType = graphene.Field(SupportedAuthnType)
    isAnonymous = graphene.Boolean()
    basiccUsername = graphene.String()
    basicPassword = graphene.String()
    bearerToken = graphene.String()
    apikeyHeader = graphene.String()
    apikey = graphene.String()
        
class ApiFuzzRequest(graphene.ObjectType):
    Id = graphene.String()
    datetime = graphene.DateTime()
    fuzzDataCaseId = graphene.String()
    fuzzcontextId = graphene.String()
    hostnamePort = graphene.String()
    verb= graphene.String()
    path = graphene.String()
    querystring= graphene.String()
    url= graphene.Scalar
    headers = graphene.List(graphene.String)
    body = graphene.String()

class ApiFuzzResponse(graphene.ObjectType):
    Id = graphene.String()
    datetime = graphene.DateTime()
    fuzzDataCaseId = graphene.String()
    httpVersion = graphene.String()
    statusCode = graphene.String()
    headers = graphene.List(graphene.String)
    body = graphene.String()
    error = graphene.String()
        

# each "fuzz data set" is one ApiFuzzCase
class ApiFuzzDataCase(graphene.ObjectType):
   id = graphene.String()
   fuzzCaseSetId = graphene.String()
   fuzzcontextId = graphene.String()
   request = graphene.Field(ApiFuzzRequest)
   response = graphene.Field(ApiFuzzResponse)
   state = graphene.Field(FuzzProgressState)
        
    
class ApiFuzzCaseSet(graphene.ObjectType):
    Id = graphene.String()
    path = graphene.String()
    querystringNonTemplate = graphene.String()
    bodyNonTemplate = graphene.String()
    selected = graphene.Boolean()
    verb = graphene.Field(ApiVerb) 
    authnType = graphene.Field(SupportedAuthnType)
    fuzzDataCases = graphene.List(ApiFuzzDataCase)
        
        
class ApiFuzzContext(graphene.ObjectType):
    Id = graphene.String()
    name = graphene.String()
    datetime = graphene.DateTime()
    
    hostname = graphene.String()
    port = graphene.Int()
    fuzzMode = graphene.String()
    fuzzcaseToExec = graphene.Int(default_value=50)
    
    requestMessageSingle = graphene.String()
    requestMessageFilePath = graphene.String()
    openapi3FilePath = graphene.String()
    openapi3Url = graphene.String()
    
    #security schemes
    authnType = graphene.Field(SupportedAuthnType)
    isAnonymous = graphene.Boolean()
    basicUsername = graphene.String()
    basicPassword  = graphene.String()
    bearerToken  = graphene.String()
    apikeyHeader  = graphene.String()
    apikey  = graphene.String()  
    fuzzcaseSets = graphene.List(ApiFuzzCaseSet)

# queries
class Query(graphene.ObjectType):
    
    fuzzcontexts = graphene.List(ApiFuzzContext)
    
    fuzzContext = graphene.Field(ApiFuzzContext, fuzzcontextId=graphene.String())
    
    def resolve_fuzzcontexts(self,info):
        
        sm = ServiceManager()
        result = sm.get_fuzzcontexts()
        return result
    
    def resolve_fuzzContext(self,info, fuzzcontextId):
        r = ApiFuzzContext()
        r.name = fuzzcontextId
        return r

# subscriptions
# class Subscription(graphene.ObjectType):
#     time_of_day = graphene.String()

#     async def subscribe_time_of_day(root, info):
#         while True:
#             yield datetime.now().isoformat()
#             await asyncio.sleep(1)

# mutations  

    
class DiscoverOpenApi3ByFilePath(graphene.Mutation):
    
    class Arguments:
        name = graphene.String()
        hostname = graphene.String()
        port = graphene.Int()
        isAnonymous = graphene.Boolean()
        username = graphene.String()
        password = graphene.String()
        bearerTokenHeader = graphene.String()
        bearerToken = graphene.String()
        apikeyHeader = graphene.String()
        apikey = graphene.String()
        openapi3FilePath = graphene.String()
    
    ok = graphene.Boolean()
    apiFuzzContext = graphene.Field(ApiFuzzContext)
    
    def mutate(self, info, hostname, port, openapi3FilePath, name='', isAnonymous=True, fuzzmode = 'Quick', numberOfFuzzcaseToExec=50, basicUsername='', basicPassword='', bearerTokenHeader = '', bearerToken='', apikeyHeader='', apikey=''):
        
        sm = ServiceManager()
        
        fuzzcontext = sm.discover_openapi3_by_filepath_or_url(
                            hostname=hostname,
                            port=port,
                            name=name,
                            fuzzMode= fuzzmode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            isAnonymous=isAnonymous,
                            basicUsername=basicUsername,
                            basicPassword=basicPassword,
                            bearerTokenHeader=bearerTokenHeader,
                            bearerToken=bearerToken,
                            apikeyHeader=apikeyHeader,
                            apikey=apikey,
                            openapi3FilePath=openapi3FilePath)
        
        ok = True
        apiFuzzContext = fuzzcontext
        
        return DiscoverOpenApi3ByFilePath(apiFuzzContext=apiFuzzContext, ok=ok)
    
class DiscoverOpenApi3ByUrl(graphene.Mutation):
    
    class Arguments:
        name = graphene.String()
        hostname = graphene.String()
        port = graphene.Int()
        isAnonymous = graphene.Boolean()
        username = graphene.String()
        password = graphene.String()
        bearerTokenHeader = graphene.String()
        bearerToken = graphene.String()
        apikeyHeader = graphene.String()
        apikey = graphene.String()
        openapi3Url = graphene.String()
    
    ok = graphene.Boolean()
    apiFuzzContext = graphene.Field(ApiFuzzContext)

   
    def mutate(self, info, hostname, port, openapi3Url, name = '', isAnonymous = True, fuzzmode = 'Quick', numberOfFuzzcaseToExec=50, basicUsername='', basicPassword='', bearerTokenHeader = '', bearerToken='', apikeyHeader='', apikey=''):
        
        sm = ServiceManager()
        
        fuzzcontext = sm.discover_openapi3_by_filepath_or_url(
                            hostname=hostname,
                            port=port,
                            name=name,
                            fuzzMode= fuzzmode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            isAnonymous=isAnonymous,
                            basicUsername=basicUsername,
                            basicPassword=basicPassword,
                            bearerTokenHeader=bearerTokenHeader,
                            bearerToken=bearerToken,
                            apikeyHeader=apikeyHeader,
                            apikey=apikey,
                            openapi3Url=openapi3Url)
        
        ok = True
        apiFuzzContext = fuzzcontext
        
        return DiscoverOpenApi3ByUrl(apiFuzzContext=apiFuzzContext, ok=ok)
    
class Fuzz(graphene.Mutation):
    class Arguments:
        fuzzcontextId = graphene.String()
        
    #define output
    ok = graphene.Boolean()
    
    async def mutate(self, info, fuzzcontextId):
        
        ok = True
        
        sm = ServiceManager()
        
        await sm.fuzz(fuzzcontextId)

        return Fuzz(ok=ok)
    
class Mutation(graphene.ObjectType):
    
    discover_by_openapi3_file_path = DiscoverOpenApi3ByFilePath.Field()
    
    discover_by_openapi3_url = DiscoverOpenApi3ByUrl.Field()
    
    fuzz = Fuzz.Field()
    
    #discoverByOpenAPI3FilePath(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    #discoverByOpenAPI3Url(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    #discoverBySingleRequestText(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    #discoverByRequestTextFilePath(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    
schema = graphene.Schema(query=Query, mutation=Mutation) #, subscription= Subscription)