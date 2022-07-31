import enum

class ApiVerb(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5

# format - generally for file property and format is binary
class ContentPropValue:
    propertyName: str = ""
    type: str = ""
    isArray: bool = False
    arrayItemType: any = None 
    nestedObjectsContent: dict = None
    format: str = None
    
    def __init__(self, propertyName, type, nestedObjectsContent: any = None, 
                 arrayItemType: any = None, isArray:bool = False, format: str = None) -> None:
        
        self.propertyName = propertyName
        self.type = type
        self.nestedObjectsContent = nestedObjectsContent
        self.arrayItemType = arrayItemType
        self.format = format
        
    def is_file_upload() -> bool:
        if type == 'string' and (format == 'binary' or format == 'base64'):
            return True
        return False
    
    
    
class UserInput:
    basicAuthUsername: str = ''
    basicAuthPassword: str = ''
    apiKeyAuthApiKey: str = ''
    bearerAuthJwtToken: str = ''
    
class Api:
    
    path: str = ''        # path includes querystring
    operationId: str = ''
    verb: ApiVerb = ApiVerb.GET
    authTypes = []
    body = {}             # for post/put/patch only
    isQueryString = True  # for get request only
    querystring = {}
    path = {}   
    
class ApiContext:
    
    baseUrl = []
    title: str = ''
    version: str = ''
    authTypes = []   # 
    apis = []
    userInput: UserInput = None