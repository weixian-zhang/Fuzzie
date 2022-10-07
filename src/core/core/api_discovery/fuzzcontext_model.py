from enum import Enum
from apicontext_model import ApiContext, ApiVerb, ContentProp, SupportedAuthnType

class FuzzProgressState(Enum):
    NOTSTARTED = "not started"
    FUZZING = "still fuzzing"
    SUCCESS = "success"
    FAILED = "failed"

class FuzzMode(Enum):
    Quick = 'quick'
    Full = 'full'
    Custom = 'custom'
    
# describes a HTTP request header, Url and/or body with hydrated with seclist data 
# A materialized request info object ready to make a HTTP call with
class ApiFuzzRequest:
    url: str = ""
    headers = {}
    body = {}       # send as Json string 

class ApiFuzzResponse:
    httpVersion: str = ""
    statusCode: str = ""
    headers = {}
    body = str      # Json string   
    error: str = ""

# each 
class ApiFuzzCase:
    id: str = ""
    data = {}
    request: ApiFuzzRequest = {}
    response: ApiFuzzResponse = {}
    state: FuzzProgressState = FuzzProgressState.NOTSTARTED

#each set is a unque http verb + path
class ApiFuzzCaseSet:     
    id: str = ""
    selected: bool = True
    path: str = ''        # path includes querystring
    verb: ApiVerb = ApiVerb.GET
    parameters: list[ContentProp]
    postBody: dict = {},
    authnType: SupportedAuthnType = SupportedAuthnType.Anonymous
    fuzzcases: list[ApiFuzzCase] = []
    
class ApiFuzzReport:
    host: str   #domain or IP include port if not default 443/80
    title: str
    requiredAuthnTypes: list[str] = []
    fuzzcaseGroups: list[ApiFuzzCaseSet] = []

# Also the data to be rendered on Fuzzie GUI client - VSCode extension and future Desktop client. 
class ApiFuzzContext:
    
    def __init__(self) -> None:
        
        # self.openapiUrl : str = ""
        # self.openapiFilePath : str = ""
        # self.requestTextFilePath : str = ""
        # self.requestTextSingle : str = ""
        
        self.hostname: str = ""
        self.port: int
        self.fuzzMode: FuzzMode = FuzzMode.Quick         
        self.fuzzcaseToExec = 50              # default 50
        self.ApiFuzzCases: list[ApiFuzzCaseSet] = []
        
        self.determine_fuzzcases()
        
        # self.apicontext: ApiContext = None  # from Api-Recognizer module
        # self.testreport : FuzzReport = None
    
    def determine_fuzzcases(self):
        
        if self.fuzzMode == FuzzMode.Quick .value:
            self.fuzzcaseToExec = 50
        elif self.fuzzMode == FuzzMode.Full.value:
            self.fuzzcaseToExec = 50000
        elif self.fuzzMode == FuzzMode.Custom.value:
            if self.fuzzcaseToExec <= 0:     # default to 50 if no value
                self.fuzzcaseToExec = 50
            
        
    

    
# Used by GUI clients to update fuzzing progress on each API
class FuzzProgress:
    testcaseId = ""
    error: str = ""
    state : FuzzProgressState = FuzzProgressState.NOTSTARTED