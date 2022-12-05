from enum import Enum

class SupportedAuthnType(Enum):
    Anonymous = "Anonymous",
    Basic = "Basic",
    Bearer = "Bearer",
    ApiKey = "ApiKey"

class ApiVerb(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = 'DELETE'
    
    
class ParameterType(Enum):
    Path = 'path'
    Query = 'query'
    Header = 'header'
    
class ArrayItem:
    
    # this class is mainly to handle future deeply nested array scenario
    # if itemType is object then parameters is dict.
    # if itemType is primitive type, parameters is None
    
    def __init__(self, type, parameters = None) -> None:
        self.type = type
        self.parameters = parameters    #for complex object only

# format - generally for file property and format is binary
# 'fileupload' is a fixed name for all file types
class ParamProp:
    
    def __init__(self, propertyName, type, parameters: any = None, arrayProp:ArrayItem = None, format='binary', paramType: str = '') -> None:
        
        self.propertyName = propertyName
        self.type = type
        self.arrayProp = arrayProp
        self.parameters = parameters
        self.format = format
        self.paramType = paramType 
        
        
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

class Api:
    def __init__(self) -> None:
        self.path: str = ''        # path includes querystring
        self.operationId: str = ''
        self.verb: ApiVerb = ApiVerb.GET
        self.authTypes = []
        self.parameters: list[ParamProp] = []
        self.body = {} 
        self.file= ''
        
class ApiContext:
    def __init__(self) -> None:
        self.baseUrl = []
        self.title: str = ''
        self.version: str = ''
        self.apis: list[Api] = []
        self.userInput: UserInput = None
        