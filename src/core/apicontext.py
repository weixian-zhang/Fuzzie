import enum

class ApiVerb(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5

class RequestBodyPropertyValue:
    type: str = ''
    format: str = None
    
    def __init__(self, type, format) -> None:
        self.type = type
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
    
    path: str = '' #path includes querystring
    operationId: str = ''
    verb: ApiVerb = ApiVerb.GET
    authTypes = []
    body = {} # for post/put/patch only
    querystring = {}    
    
class ApiContext:
    
    baseUrl = []
    title: str = ''
    version: str = ''
    authTypes = []
    apis = []
    userInput: UserInput = None