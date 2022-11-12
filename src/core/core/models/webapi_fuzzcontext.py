from datetime import datetime
from enum import Enum
from apicontext import ApiVerb, SupportedAuthnType
import jsonpickle

# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
# from sqlalchemy.orm import relationship, backref, object_session
# from sqlalchemy.ext.declarative import declarative_base

#sqlalchemy query from Model itself
#ref: https://stackoverflow.com/questions/14337244/how-to-query-inside-a-class-in-sqlalchemy

# SqlAlchemyBase = declarative_base()

class FuzzProgressState(Enum):
    NOTSTARTED = "not started"
    FUZZING = "still fuzzing"
    SUCCESS = "success"
    FAILED = "failed"

class FuzzMode(Enum):
    Quick = 'quick'
    Full = 'full'
    Custom = 'custom'

# rfc 2616
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html
# describes a HTTP request header, Url and/or body with hydrated with seclist data 
# A materialized request info object ready to make a HTTP call with
class ApiFuzzRequest:
    
    def __init__(self) -> None:
        self.Id: str = ''
        self.datetime: datetime 
        self.fuzzDataCaseId: str = ''
        self.fuzzcontextId = ''
        self.hostnamePort = ''
        self.verb = ''
        self.path: str = ''
        self.querystring: str = ''
        self.url: str = ''
        self.headers = {}    # json 
        self.body = {}       # json 
        self.requestMessage = ''

# rfc 2616
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6
class ApiFuzzResponse:
    def __init__(self) -> None:
        self.Id: str
        self.datetime: datetime
        self.fuzzDataCaseId = ''
        self.fuzzcontextId = ''
        self.statusCode = ''
        self.reasonPharse = ''
        self.responseDisplayText = ''
        self.headerJson = ''
        self.setcookieHeader = ''
        self.body = ''

class ApiFuzzCaseSetRun:
    
    def __init__(self, id, fuzzcontextId, fuzzdatacaseId) -> None:  
        self.Id: str = id
        self.datetime = ''
        self.fuzzcontextId = fuzzcontextId

# each fuzz data case is a unique verb + path + fuzz data
class ApiFuzzDataCase:
    
    def __init__(self) -> None:  
        self.Id: str = ''
        self.fuzzCaseSetId = ''
        self.fuzzCaseSetRunId = ''
        self.fuzzcontextId = ''
        self.request: ApiFuzzRequest = {}
        self.response: ApiFuzzResponse = {}
        
    def json(self):
       return jsonpickle.encode(self, unpicklable=False)

# each "fuzz data set" is one a unique verb + path
class ApiFuzzCaseSet:
    
    def __init__(self) -> None:  
        self.Id: str = ''
        self.selected: bool = True          # to be use in future to support GUI select 1 or more API to fuzz instead of default all APIs
        self.verb: ApiVerb = ApiVerb.GET
        self.fuzzcontextId = ''
        self.fuzzDataCases: list[ApiFuzzDataCase] = []
        
        # "original" non jinja data template strings
        self.path = ''
        self.querystringNonTemplate = ''
        self.bodyNonTemplate = ''
        self.headerNonTemplate = ''
        

        self.pathDataTemplate = ''
        self.querystringDataTemplate = ''
        self.bodyDataTemplate = ''
        self.headerDataTemplate = {}

    def get_path_datatemplate(self):
        if not self.pathDataTemplate.startswith('/'):
            self.pathDataTemplate = '/' + self.pathDataTemplate
        return self.pathDataTemplate


# Also the data to be rendered on Fuzzie GUI client - VSCode extension and future Desktop client. 
class ApiFuzzContext:
    
    def __init__(self) -> None:
        self.Id: str = ''
        self.datetime: datetime
        self.name = ''
        self.apiDiscoveryMethod = ''
        self.requestTextContent = ''
        self.requestTextFilePath = ''
        self.openapi3FilePath = ''
        self.openapi3Url = ''
        self.openapi3Content = ''

        #security scheme
        self.isanonymous = False
        self.basicUsername = ''
        self.basicPassword = '' 
        self.bearerTokenHeader = ''
        self.bearerToken= ''
        self.apikeyHeader=  '' 
        self.apikey= '' 
        
        # execution
        self.hostname: str = ''
        self.port: int   
        self.fuzzcaseToExec = 100
        self.authnType: str = SupportedAuthnType.Anonymous.name
        
        self.fuzzcaseSets: list[ApiFuzzCaseSet] = []
        #self.fuzzExecutionConfig: FuzzExecutionConfig
        
        #self.determine_num_of_fuzzcases(self.fuzzExecutionConfig)
    
    def get_hostname_port(self):
        if self.port == '':
            return self.hostname
        return f'{self.hostname}:{self.port}'
        
class ApiFuzzReport:
    def __init__(self) -> None:
        self.host: str   #domain or IP include port if not default 443/80
        self.title: str
        self.requiredAuthnTypes: list[str] = []
        self.fuzzcaseSet: list[ApiFuzzCaseSet] = []
    
# Used by GUI clients to update fuzzing progress on each API
class FuzzProgress:
    testcaseId = ''
    error: str = ''
    state : FuzzProgressState = FuzzProgressState.NOTSTARTED
    

class WSMsg_Fuzzing_FuzzCaseSetSummary:
    def __init__(self,fuzzCaseSetId, statusCode) -> None:
        self.fuzzCaseSetId = fuzzCaseSetId
        self.statusCode = statusCode