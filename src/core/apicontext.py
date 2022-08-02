import enum

class ApiVerb(enum.Enum):
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
    # if itemType is array type, itemContent is the type of the item in nested array. E.g: integer in the below case
        # supports only 1 level of array item for now. [[1,2,3], [4,5,6]]
    type: str = ""          
    itemContent: any = None
    
    def __init__(self, type, itemContent = None) -> None:
        self.type = type
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