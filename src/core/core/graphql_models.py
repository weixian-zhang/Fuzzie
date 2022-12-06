from datetime import datetime
import graphene

        
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

class FuzzerStatus(graphene.ObjectType):
    timestamp = graphene.String()
    alive = graphene.Boolean()
    isDataLoaded = graphene.Boolean()
    message = graphene.String()

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

# class ApiFuzzContext_Runs_ViewModel(graphene.ObjectType):
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
#     fuzzcaseSets = graphene.List(ApiFuzzCaseSetViewModel)

# class ApiFuzzCaseSet_RunSummary_ViewModel(graphene.ObjectType):
#     Id: graphene.String()
#     http2xx = graphene.Int()
#     http3xx = graphene.Int()
#     http4xx = graphene.Int()
#     http5xx =  graphene.Int()
#     completedDataCaseRuns = graphene.Int() 

class ApiFuzzCaseSetUpdate(graphene.InputObjectType):
    fuzzCaseSetId = graphene.String()
    selected = graphene.Boolean()
    
class ApiFuzzContextUpdate(graphene.InputObjectType):
    fuzzcontextId = graphene.String()
    name = graphene.String()
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
    
class ApiFuzzCaseSets_With_RunSummary_ViewModel(graphene.ObjectType):
    fuzzCaseSetId = graphene.String()
    fuzzCaseSetRunId = graphene.String()
    fuzzcontextId = graphene.String()
    selected = graphene.Boolean()
    verb = graphene.Field(ApiVerb) 
    path = graphene.String()
    querystringNonTemplate = graphene.String()
    bodyNonTemplate = graphene.String()
    headerNonTemplate = graphene.String()
    authnType = graphene.Field(SupportedAuthnType)
    
    runSummaryId = graphene.String()
    http2xx = graphene.Int()
    http3xx = graphene.Int()
    http4xx = graphene.Int()
    http5xx =  graphene.Int()
    completedDataCaseRuns = graphene.Int() 
    
class ApiFuzzCaseSetRunViewModel(graphene.ObjectType):
    fuzzCaseSetRunsId = graphene.String()
    fuzzcontextId = graphene.String()
    startTime = graphene.DateTime()
    endTime =  graphene.DateTime()
    status = graphene.String()
    

class ApiFuzzContext_Runs_ViewModel(graphene.ObjectType):
    
    Id = graphene.String()
    datetime = graphene.DateTime()
    name = graphene.String()
    apiDiscoveryMethod = graphene.String()
    requestTextContent = graphene.String()
    requestTextFilePath = graphene.String()
    openapi3FilePath = graphene.String()
    openapi3Url = graphene.String()
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
    
    # CaseSetRun
    fuzzCaseSetRuns = graphene.List(ApiFuzzCaseSetRunViewModel)
    
class FuzzContextRunQueryResult(graphene.ObjectType):
    ok = graphene.Boolean()
    error = graphene.String()
    result = graphene.List(ApiFuzzContext_Runs_ViewModel)
    
class FuzzCaseSetRunSummaryQueryResult(graphene.ObjectType):
    ok = graphene.Boolean()
    error = graphene.String()
    result = graphene.List(ApiFuzzCaseSets_With_RunSummary_ViewModel)
    
    def __init__(self, ok, error, result) -> None:
        super().__init__()
        
        ok = ok
        error = error
        result = result
