import enum

class ApiVerb(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5
    
# apiAuthType = {
#     'basicAuth': BasicAuth = 1
#     ApiKeyAuth = 2
#     BearerAuth = 3
#     NoAuth = 4
# }

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
    
class ApiContext:
    
    baseUrl = []
    title: str = ''
    version: str = ''
    authTypes = []
    apis = []

class Api:
    
    path: str = '' #path includes querystring
    operationId: str = ''
    verb: ApiVerb = ApiVerb.GET
    authTypes = []
    body = {} # for post/put/patch only
    querystring = {}    