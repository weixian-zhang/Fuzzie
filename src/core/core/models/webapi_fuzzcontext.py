from datetime import datetime
from enum import Enum
from apicontext import ApiVerb, SupportedAuthnType

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

# rfc 2616
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6
class ApiFuzzResponse:
    def __init__(self) -> None:
        self.Id: str = ''
        self.datetime: datetime
        self.fuzzDataCaseId: str = ''
        self.fuzzcontextId = ''
        self.statusCode: str = ''
        self.reasonPharse: str = ''
        self.responseJson = ''
        self.setcookieHeader = ''
        self.content = str      # json   

# each fuzz data case is a unique verb + path + fuzz data
class ApiFuzzDataCase:
    
    def __init__(self) -> None:  
        self.Id: str = ''
        self.fuzzCaseSetId = ''
        self.fuzzcontextId = ''
        self.request: ApiFuzzRequest = {}
        self.response: ApiFuzzResponse = {}
        self.progressState = ''                     #FuzzProgressState.NOTSTARTED

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
        
        # all ApiFuzzDataCase generate new data base on this template. This template is a json string with 
        # property name and value as data-type. Base on data-type fuzzer calls DataFactory.{data type} to generate tjhe correct
        # fuzz data for that data-type
        self.pathDataTemplate: str = ''
        self.querystringDataTemplate: str = ''
        self.bodyDataTemplate: str = ''
        self.headerDataTemplate = {}

    
    # path + querystring data templates combined
    def get_path_datatemplate(self):
        if not self.pathDataTemplate.startswith('/'):
            self.pathDataTemplate = '/' + self.pathDataTemplate
        return self.pathDataTemplate
    
    def get_querystring_datatemplate(self):
        return self.querystringDataTemplate


# Also the data to be rendered on Fuzzie GUI client - VSCode extension and future Desktop client. 
class ApiFuzzContext:
    
    def __init__(self) -> None:
        self.Id: str = ''
        self.datetime: datetime
        self.name = ''
        self.requestMessageSingle = ''
        self.requestMessageFilePath = ''
        self.openapi3FilePath = ''
        self.openapi3Url = ''
        
        # execution
        self.hostname: str = ''
        self.port: int
        self.fuzzMode: FuzzMode = FuzzMode.Quick         
        self.fuzzcaseToExec = 100
        
        #security schemes
        self.authnType : SupportedAuthnType = SupportedAuthnType.Anonymous
        self.isAnonymous = False
        self.basicUsername = ''
        self.basicPassword  = ''
        self.bearerTokenHeader = ''
        self.bearerToken  = ''
        self.apikeyHeader  = ''
        self.apikey  = ''
        
        self.fuzzcaseSets: list[ApiFuzzCaseSet] = []
        #self.fuzzExecutionConfig: FuzzExecutionConfig
        
        #self.determine_num_of_fuzzcases(self.fuzzExecutionConfig)
    
    def get_hostname_port(self):
        if self.port == '':
            return self.hostname
        return f'{self.hostname}:{self.port}'
                
    def is_basic_authn(self):
        if self.get_security_scheme() == SupportedAuthnType.Basic:
            return True
        return False
    
    def is_bearertoken_authn(self):
        if self.get_security_scheme() == SupportedAuthnType.Bearer:
            return True
        return False
    
    def is_apikey_authn(self):
        if self.get_security_scheme() == SupportedAuthnType.ApiKey:
            return True
        return False
                
    def get_security_scheme(self) -> SupportedAuthnType:
        if self.isAnonymous == True:
            return SupportedAuthnType.Anonymous
        elif self.basicUsername != '' and self.basicPassword != '':
            return SupportedAuthnType.Basic
        elif self.bearerToken != '':
            return SupportedAuthnType.Bearer
        elif self.apikeyHeader != '' and self.apikey != '':
            return SupportedAuthnType.ApiKey
        else:
            return SupportedAuthnType.Anonymous
        
        
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