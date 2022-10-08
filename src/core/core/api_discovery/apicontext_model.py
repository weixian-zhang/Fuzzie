from enum import Enum

class SupportedAuthnType(Enum):
    Anonymous = "Anonymous",
    Basic = "Basic",
    Bearer = "Bearer",
    ApiKey = "ApiKey",
    ApiKeyCookie = "ApiKeyCookie"

class ApiVerb(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    
class ArrayItem:
    
    # this class is mainly to handle future deeply nested array scenario
    # if itemType is object then parameters is dict.
    # if itemType is primitive type, parameters is None
        # supports only 1 level of array item for now. [[1,2,3], [4,5,6]]
    type: str = ""       
    parameters: dict = {}      #for objects in array
    
    def __init__(self, type, parameters = None) -> None:
        self.type = type
        self.parameters = parameters

# format - generally for file property and format is binary
class ParamProp:
    propertyName: str = ""
    type: str = ""
    arrayProp: ArrayItem = None
    parameters: dict = None
    format: str = None
    getApiParamIn: str = '' #only for GetApi, determines parameter In path, query, cookie, header
    
    def __init__(self, propertyName, type, parameters: any = None, arrayProp:ArrayItem = None, format: str = None, getApiParamIn = '') -> None:
        
        self.propertyName = propertyName
        self.type = type
        self.parameters = parameters
        self.format = format
        self.getApiParamIn = getApiParamIn
        self.arrayProp = arrayProp
        
    def is_file_upload() -> bool:
        if type == 'string' and (format == 'binary' or format == 'base64'):
            return True
        return False


    
class UserInput:
    basicAuthUsername: str = ''
    basicAuthPassword: str = ''
    apiKeyAuthApiKey: str = ''
    bearerAuthJwtToken: str = ''

class BaseApi:
    path: str = ''        # path includes querystring
    operationId: str = ''
    verb: ApiVerb = ApiVerb.GET
    authTypes = []   
    headerParameters: list[ParamProp] = []
    
class GetApi(BaseApi):
    paramIn: str = ''
    parameters: list[ParamProp] = []
    
class MutatorApi(BaseApi):
    body = {} 
    
class Api:
    
    path: str = ''        # path includes querystring
    operationId: str = ''
    verb: ApiVerb = ApiVerb.GET
         # not in use, instead use authn type from ApiContext
    body = {}             # for post/put/patch only
    isQueryString = True  # for get request only
    parameters: list[ParamProp] = [] 
    headerParameters: list[ParamProp] = []

class ApiAuthnBasic:
    username = ""
    password = ""
    
class ApiAuthnBearerToken:
    token = ""
    
class ApiAuthnApiKey:
    headerName = ""
    apikey = ""
    
class ApiAuthnApiKeyCookie:
    cookieName = ""
    cookieValue = ""
    
class ApiContext:
    
    baseUrl = []
    title: str = ''
    version: str = ''
    #authTypes = []      # to be removed permanantly. User will input the choice of authn
    apis = []
    userInput: UserInput = None
    authnType : SupportedAuthnType = SupportedAuthnType.Anonymous
    basicAuthn: ApiAuthnBasic = None
    bearerTokenAuthn: ApiAuthnBearerToken = None
    apikeyAuthn: ApiAuthnApiKey = None
    apikeyCookieAuthn: ApiAuthnApiKeyCookie = None