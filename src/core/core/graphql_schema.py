import graphene

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
    Cookie = 'cookie'

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
    datetime= graphene.DateTime()
    path = graphene.String()
    querystring= graphene.String()
    url= graphene.Scalar
    headers = graphene.List(graphene.String)
    cookies = graphene.List(graphene.String)
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
   fuzzcaseId = graphene.String()
   request = graphene.Field(ApiFuzzRequest)
   response = graphene.Field(ApiFuzzResponse)
   state = graphene.Field(FuzzProgressState)
        
    
class ApiFuzzCaseSet(graphene.ObjectType):
    Id = graphene.String()
    selected = graphene.Boolean()
    verb = graphene.Field(ApiVerb) 
    authnType = graphene.Field(SupportedAuthnType)
    fuzzDataCases = graphene.List(graphene.Field(ApiFuzzDataCase))

class FuzzExecutionConfig(graphene.ObjectType):
    hostname = graphene.String()
    port = graphene.Int()
    fuzzMode =graphene.Field(ApiVerb)
    fuzzcaseToExec = graphene.Int(default_value=50)
    securitySchemes = graphene.Field(SecuritySchemes)
        
        
class ApiFuzzContext(graphene.ObjectType):
    Id = graphene.String()
    name = graphene.String()
    datetime: graphene.DateTime()
    
    hostname = graphene.String()
    port = graphene.Int()
    fuzzMode = graphene.Field(FuzzMode)
    fuzzcaseToExec = graphene.Int(default_value=50)
    
    #security schemes
    authnType = graphene.Field(SupportedAuthnType)
    isAnonymous = graphene.Boolean()
    basicUsername = graphene.String()
    basicPassword  = graphene.String()
    bearerToken  = graphene.String()
    apikeyHeader  = graphene.String()
    apikey  = graphene.String()
    
    fuzzcaseSets: graphene.List(graphene.Field(ApiFuzzCaseSet))
    fuzzExecutionConfig = graphene.Field(FuzzExecutionConfig)

# queries
class Query(graphene.ObjectType):
    
    fuzzcontexts = graphene.List(ApiFuzzContext)
    
    fuzzContext = graphene.Field(type=ApiFuzzContext, fuzzcontextId=graphene.String())
    
    def resolve_fuzzcontexts(self,info):
        return [None]
    
    def resolve_fuzzContext(self,info, fuzzcontextId):
        r = ApiFuzzContext()
        r.name = fuzzcontextId
        return r

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
    
    ok = graphene.Boolean()
    apiFuzzContext = graphene.Field(ApiFuzzContext)
    
    def mutate(self, info, name, hostname, port, isAnonymous, username='', password='', bearerToken='', apikeyHeader='', apikey=''):
        apiFuzzContext = ApiFuzzContext()
        apiFuzzContext.name = name
        apiFuzzContext.hostname = hostname
        apiFuzzContext.port = port
        
        ok = True
        return DiscoverOpenApi3ByFilePath(apiFuzzContext=apiFuzzContext, ok=ok)
    
class Mutation(graphene.ObjectType):
    
    discover_by_openapi3_file_path = DiscoverOpenApi3ByFilePath.Field()
    
    #discoverByOpenAPI3FilePath(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    #discoverByOpenAPI3Url(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    #discoverBySingleRequestText(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    
    #discoverByRequestTextFilePath(hostname, port, username, password, bearerToken, apikeyHeader, apikey)
    

# subscription
# only used when a fuzz test happens as Fuzzie needs to report to GUI client, the status of each API in fuzz-operation
class Subscription(graphene.ObjectType):
    pass
    
    
schema = graphene.Schema(query=Query, mutation=Mutation) #, subscription= Subscription)