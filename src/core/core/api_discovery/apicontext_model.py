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
    
    def __init__(self, type, parameters = None) -> None:
        self.type = type
        self.parameters = parameters    #for complex object only

# format - generally for file property and format is binary
class ParamProp:
    
    def __init__(self, propertyName, type, parameters: any = None, arrayProp:ArrayItem = None, format: str = None, getApiParamIn = '') -> None:
        
        self.propertyName = propertyName
        self.type = type
        self.arrayProp = arrayProp
        self.parameters = parameters
        self.format = format
        self.getApiParamIn = getApiParamIn  #only for GetApi, determines parameter In path, query, cookie, header
        
        
    def is_file_upload() -> bool:
        if type == 'string' and (format == 'binary' or format == 'base64'):
            return True
        return False


    
class UserInput:
    def __init__(self) -> None:
        self.basicAuthUsername: str = ''
        self.basicAuthPassword: str = ''
        self.apiKeyAuthApiKey: str = ''
        self.bearerAuthJwtToken: str = ''

class BaseApi:
    def __init__(self) -> None:
        self.path: str = ''        # path includes querystring
        self.operationId: str = ''
        self.verb: ApiVerb = ApiVerb.GET
        self.authTypes = []   
        self.headerParameters: list[ParamProp] = []
    
class GetApi(BaseApi):
    def __init__(self) -> None:
        self.paramIn: str = ''
        self.parameters: list[ParamProp] = []
    
class MutatorApi(BaseApi):
    def __init__(self) -> None:
        self.body = {} 
    
class Api:
    def __init__(self) -> None:
        self.path: str = ''        # path includes querystring
        self.operationId: str = ''
        self.verb: ApiVerb = ApiVerb.GET
        self.body = {}             # for post/put/patch only
        self.isQueryString = True  # for get request only
        self.parameters: list[ParamProp] = [] 
        self.headerParameters: list[ParamProp] = []

class ApiAuthnBasic:
    def __init__(self) -> None:
        self.username = ''
        self.password = ''
    
class ApiAuthnBearerToken:
    def __init__(self) -> None:
        self.token = ''
    
class ApiAuthnApiKey:
    def __init__(self) -> None:
        self.headerName = ''
        self.apikey = ''
    
class ApiAuthnApiKeyCookie:
    
    def __init__(self) -> None:
        self.cookieName = ''
        self.cookieValue = ''
    
class ApiContext:
    def __init__(self) -> None:
        self.baseUrl = []
        self.title: str = ''
        self.version: str = ''
        self.apis = []
        self.userInput: UserInput = None
        self.authnType : SupportedAuthnType = SupportedAuthnType.Anonymous
        self.basicAuthn: ApiAuthnBasic = None
        self.bearerTokenAuthn: ApiAuthnBearerToken = None
        self.apikeyAuthn: ApiAuthnApiKey = None
        self.apikeyCookieAuthn: ApiAuthnApiKeyCookie = None