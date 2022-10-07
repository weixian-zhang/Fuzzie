from enum import Enum

class SupportedAuthnType(Enum):
    Anonymous = "Anonymous",
    Basic = "Basic",
    Bearer = "Bearer",
    ApiKey = "ApiKey",
    ApiKeyCookie = "ApiKeyCookie"

class ApiVerb(Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5

# format - generally for file property and format is binary
class ContentProp:
    propertyName: str = ""
    type: str = ""
    isArray: bool = False
    nestedContent: dict = None
    format: str = None
    
    def __init__(self, propertyName, type, nestedContent: any = None, 
                 arrayItemType: any = None, isArray:bool = False, format: str = None) -> None:
        
        self.propertyName = propertyName
        self.type = type
        self.nestedContent = nestedContent
        self.arrayItemType = arrayItemType
        self.format = format
        
    def is_file_upload() -> bool:
        if type == 'string' and (format == 'binary' or format == 'base64'):
            return True
        return False

class ArrayItem:
    
    # this class is mainly to handle future deeply nested array scenario
    # if itemType is object then itemContent is dict.
    # if itemType is primitive type, itemContent is None
    # if itemType is array type, innerArrayItemType is the type of the item in nested array. E.g: integer in the below case
        # supports only 1 level of array item for now. [[1,2,3], [4,5,6]]
    itemType: str = ""    
    innerArrayItemType: str = ""      
    itemContent: any = None
    
    def __init__(self, itemType, innerArrayItemType= "", itemContent = None) -> None:
        self.itemType = itemType
        self.innerArrayItemType = innerArrayItemType
        self.itemContent = itemContent
    
class UserInput:
    basicAuthUsername: str = ''
    basicAuthPassword: str = ''
    apiKeyAuthApiKey: str = ''
    bearerAuthJwtToken: str = ''
    
class Api:
    
    path: str = ''        # path includes querystring
    operationId: str = ''
    verb: ApiVerb = ApiVerb.GET
    authTypes = []        # not in use, instead use authn type from ApiContext
    body = {}             # for post/put/patch only
    isQueryString = True  # for get request only
    parameters: list[ContentProp] = [] 
    headerParameters: list[ContentProp] = []

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