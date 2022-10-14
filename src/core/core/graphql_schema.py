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

class AuthnBasic(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()
        
    
class AuthnBearerToken(graphene.ObjectType):
    headerName = graphene.String()
    token = graphene.String()
    
class AuthnApiKey(graphene.ObjectType):
    headerName = graphene.String()
    apikey = graphene.String()

class SecuritySchemes(graphene.ObjectType):
    authnType = graphene.Field(SupportedAuthnType)
    isAnonymous = graphene.Boolean()
    basicAuthn = graphene.Field(AuthnBasic)
    bearerTokenAuthn = graphene.Field(AuthnBearerToken)
    apikeyAuthn = graphene.Field(AuthnBearerToken)
        
        
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
    Id: str = graphene.String()
    datetime: graphene.DateTime()
    fuzzcaseSets: graphene.List(graphene.Field(ApiFuzzCaseSet))
    fuzzExecutionConfig = graphene.Field(FuzzExecutionConfig)
    
class Query(graphene.ObjectType):
    
    fuzzcontexts = graphene.List(ApiFuzzContext)
    
    def resolve_fuzzcontexts(self,info):
        return [None]
    
    
    
schema = graphene.Schema(query=Query)