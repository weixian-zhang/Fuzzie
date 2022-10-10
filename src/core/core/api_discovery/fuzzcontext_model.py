from enum import Enum
from apicontext_model import ApiContext, ApiVerb, ParamProp, SupportedAuthnType

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
    def __init__(self) -> None:  
        self.url: str = ''
        self.querystring: str = ''
        self.headers = {}
        self.cookies = {}
        self.body = {}       # json string 

class ApiFuzzResponse:
    def __init__(self) -> None:  
        self.httpVersion: str = ''
        self.statusCode: str = ''
        self.headers = {}
        self.body = str      # json string   
        self.error: str = ''

# each "fuzz data set" is one ApiFuzzCase
class ApiFuzzDataCase:
    def __init__(self) -> None:  
        self.id: str = ''
        self.data = {}
        self.request: ApiFuzzRequest = {}
        self.response: ApiFuzzResponse = {}
        self.state: FuzzProgressState = FuzzProgressState.NOTSTARTED

class ApiFuzzCaseSet:
    def __init__(self) -> None:  
        self.id: str = ''
        self.selected: bool = True
        self.path: str = '' 
        self.querystring: str = ''
        self.headers = {}
        self.cookie = {}
        self.body: str = ''
        self.verb: ApiVerb = ApiVerb.GET
        self.authnType: SupportedAuthnType = SupportedAuthnType.Anonymous
        self.fuzzDataCases: list[ApiFuzzDataCase] = []
    
        # all ApiFuzzDataCase generate new data base on this template. This template is a json string with 
        # property name and value as data-type. Base on data-type fuzzer calls DataFactory.{data type} to generate tjhe correct
        # fuzz data for that data-type
        self.pathDataTemplate = {}
        self.querystringDataTemplate = {}
        self.headergDataTemplate = {}
        self.cookieDataTemplate = {}
        self.bodyDataTemplate = {}
    
#each set is a unque http verb + path
# class GetApiFuzzCaseSet(ApiFuzzCaseSet): 
#     def __init__(self) -> None:    
#         self.paramIn: str = 'path'
#         self.paramProperties = list[ParamProp]
#         self.verb: ApiVerb = ApiVerb.POST
    
# class MutatorApiFuzzCaseSet(ApiFuzzCaseSet):
#     def __init__(self) -> None:
#         self.bodyParamProperties: list[ParamProp] = []
#         self.verb: ApiVerb = ApiVerb.GET
    
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
        
class SecuritySchemes:
    
    def __init__(self) -> None:
        self.authnType : SupportedAuthnType = SupportedAuthnType.Anonymous
        self.basicAuthn: ApiAuthnBasic = None
        self.bearerTokenAuthn: ApiAuthnBearerToken = None
        self.apikeyAuthn: ApiAuthnApiKey = None
        self.apikeyCookieAuthn: ApiAuthnApiKeyCookie = None
          
class ApiFuzzReport:
    def __init__(self) -> None:
        self.host: str   #domain or IP include port if not default 443/80
        self.title: str
        self.requiredAuthnTypes: list[str] = []
        self.fuzzcaseSet: list[ApiFuzzCaseSet] = []
        
class FuzzExecutionConfig:
    
    def __init__(self) -> None:
        self.hostname: str = ''
        self.port: int
        self.fuzzMode: FuzzMode = FuzzMode.Quick         
        self.fuzzcaseToExec = 50              # default 50
        self.securitySchemes: SecuritySchemes = SecuritySchemes()


# Also the data to be rendered on Fuzzie GUI client - VSCode extension and future Desktop client. 
class ApiFuzzContext:
    
    def __init__(self) -> None:
        
        self.fuzzcaseSets: list[ApiFuzzCaseSet] = []
        self.fuzzExecutionConfig: FuzzExecutionConfig
        
        #self.determine_num_of_fuzzcases(self.fuzzExecutionConfig)
    
    def determine_numof_fuzzcases_to_run(self):
        
        if self.fuzzExecutionConfig.fuzzMode == FuzzMode.Quick .value:
            self.fuzzExecutionConfig.fuzzcaseToExec = 50
        elif self.fuzzExecutionConfig.fuzzMode == FuzzMode.Full.value:
            self.fuzzExecutionConfig.fuzzcaseToExec = 50000
        elif self.fuzzExecutionConfig.fuzzMode == FuzzMode.Custom.value:
            if self.fuzzExecutionConfig.fuzzcaseToExec <= 0:     # default to 50 if no value
                self.fuzzExecutionConfig.fuzzcaseToExec = 50
            

    
# Used by GUI clients to update fuzzing progress on each API
class FuzzProgress:
    testcaseId = ''
    error: str = ''
    state : FuzzProgressState = FuzzProgressState.NOTSTARTED