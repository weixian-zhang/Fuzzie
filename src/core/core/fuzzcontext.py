from enum import Enum
from apicontext import ApiContext, ApiVerb, ContentProp, SupportedAuthnType

class FuzzProgressState(Enum):
    NOTSTARTED = "not started"
    FUZZING = "still fuzzing"
    SUCCESS = "success"
    FAILED = "failed"

    
    
# describes a HTTP request header, Url and/or body with hydrated with seclist data 
# A materialized request info object ready to make a HTTP call with
class FuzzRequest:
    url: str = ""
    headers = {}
    body = {}       # send as Json string 

class FuzzResponse:
    httpVersion: str = ""
    status: str = ""
    headers = {}
    body = str      # Json string   
    error: str = ""

class FuzzCase:
    id: str = ""
    data = {}
    request: FuzzRequest = {}
    response: FuzzResponse = {}
    state: FuzzProgressState = FuzzProgressState.NOTSTARTED
    
class FuzzCaseGroup:
    id: str = ""
    path: str = ''        # path includes querystring
    verb: ApiVerb = ApiVerb.GET
    parameters: list[ContentProp]
    postBody: dict = {},
    authnType: SupportedAuthnType = SupportedAuthnType.Anonymous
    fuzzcases: list[FuzzCase] = []
    
class FuzzReport:
    host: str   #domain or IP include port if not default 443/80
    title: str
    requiredAuthnTypes: list[str] = []
    fuzzcaseGroups: list[FuzzCaseGroup] = []

# Also the data to be rendered on Fuzzie GUI client - VSCode extension and future Desktop client. 
class FuzzContext:
    
    def __init__(self) -> None:
        
        self.openapiUrl : str = ""
        self.openapiFilePath : str = ""
        self.requestTextFilePath : str = ""
        self.requestTextSingle : str = ""
        
        self.apicontext: ApiContext = None  # from Api-Recognizer module
        self.testreport : FuzzReport = None
        
    

    
# Used by GUI clients to update fuzzing progress on each API
class FuzzProgress:
    testcaseId = ""
    state : FuzzProgressState = FuzzProgressState.NOTSTARTED
    pass 