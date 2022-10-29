from webapi_fuzzcontext import FuzzMode, SupportedAuthnType, ApiFuzzCaseSet, ApiVerb
from datetime import datetime
import graphene

# class ApiFuzzCaseSetView:
#     def __init__(self):
#         self.Id: str = ''
#         self.selected: bool = True          # to be use in future to support GUI select 1 or more API to fuzz instead of default all APIs
#         self.verb = ''
#         self.fuzzcontextId = ''
#         self.path = ''
#         self.querystringNonTemplate = ''
#         self.bodyNonTemplate = ''
#         self.headerNonTemplate = ''
        
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
    selected = graphene.Boolean()
    verb = graphene.Field(ApiVerb) 
    path = graphene.String()
    querystringNonTemplate = graphene.String()
    bodyNonTemplate = graphene.String()
    headerNonTemplate = graphene.String()
    authnType = graphene.Field(SupportedAuthnType)
        
        
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
    basicUsername = graphene.String()
    basicPassword  = graphene.String()
    bearerToken  = graphene.String()
    apikeyHeader  = graphene.String()
    apikey  = graphene.String()  
    fuzzcaseSets = graphene.List(ApiFuzzCaseSet)

class ApiFuzzContextSetsRunsView:
    contextId = graphene.String()
    datetime = graphene.DateTime()
    name = graphene.String()
    requestMessageSingle = ''
    requestMessageFilePath = ''
    openapi3FilePath = ''
    openapi3Url = ''
    hostname: str = ''
    port: int
    fuzzMode: FuzzMode = FuzzMode.Quick         
    fuzzcaseToExec = 100
    authnType: str = SupportedAuthnType.Anonymous.name
    caseSetRunsId = ''
    caseSetViews: list[ApiFuzzCaseSet] = []