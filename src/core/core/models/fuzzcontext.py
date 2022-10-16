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
    
    # __tablename__ = 'ApiFuzzRequest'
    # Id = Column(String, primary_key=True)
    # datetime = Column(DateTime)
    # path = Column(String)
    # querystring = Column(String)
    # url = Column(String)
    # headers = Column(String)
    # cookies = Column(String)
    # body = Column(String)
    
    # fuzzDataCaseId = Column(Integer, ForeignKey("ApiFuzzDataCase.Id"))
    
    def __init__(self) -> None:
        self.Id: str = ''
        self.datetime: datetime 
        self.fuzzDataCaseId: str = ''
        self.datetime: datetime
        self.path: str = ''
        self.querystring: str = ''
        self.url: str = ''
        self.headers = {}    # json 
        self.cookies = {}    # json 
        self.body = {}       # json 

# rfc 2616
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6
class ApiFuzzResponse:
    def __init__(self) -> None:
        self.Id: str = ''
        self.datetime: datetime
        self.fuzzDataCaseId: str = ''
        self.statusCode: str = ''
        self.reasonPharse: str = ''
        self.headers = {}    # json
        self.body = str      # json   

# each fuzz data case is a unique verb + path + fuzz data
class ApiFuzzDataCase:
    
    # __tablename__ = 'ApiFuzzDataCase'
    # Id = Column(String, primary_key=True)
    # fuzzCaseSetId = Column(Integer, ForeignKey("ApiFuzzCaseSet.Id"))
    
    def __init__(self) -> None:  
        self.Id: str = ''
        self.fuzzcaseId: str = ''
        self.request: ApiFuzzRequest = {}
        self.response: ApiFuzzResponse = {}
        self.state: FuzzProgressState = FuzzProgressState.NOTSTARTED

# each "fuzz data set" is one a unique verb + path
class ApiFuzzCaseSet:
    
    # __tablename__ = 'ApiFuzzCaseSet'
    # Id = Column(String, primary_key=True)
    # selected = Column(Boolean)
    # verb = Column(String)
    # pathDataTemplate = Column(String)
    # querystringDataTemplate = Column(String)
    # headerDataTemplate = Column(String)         # json
    # cookieDataTemplate = Column(String)         # json
    # bodyDataTemplate = Column(String)           # json
    # fuzzcontextId = Column(Integer, ForeignKey("ApiFuzzContext.Id"))
    
    def __init__(self) -> None:  
        self.Id: str = ''
        self.selected: bool = True
        self.verb: ApiVerb = ApiVerb.GET
        self.fuzzcontextId = ''
        self.fuzzDataCases: list[ApiFuzzDataCase] = []
    
        # all ApiFuzzDataCase generate new data base on this template. This template is a json string with 
        # property name and value as data-type. Base on data-type fuzzer calls DataFactory.{data type} to generate tjhe correct
        # fuzz data for that data-type
        self.pathDataTemplate: str = ''
        self.querystringDataTemplate: str = ''
        self.headerDataTemplate = {}
        self.cookieDataTemplate = {}
        self.bodyDataTemplate: str = ''
        
    # path + querystring data templates combined
    def get_url_datatemplate(self):
        return self.pathDataTemplate + self.querystringDataTemplate


# Also the data to be rendered on Fuzzie GUI client - VSCode extension and future Desktop client. 
class ApiFuzzContext:
    
    # __tablename__ = 'ApiFuzzContext'
    # Id = Column(String, primary_key=True)
    # datetime = Column(DateTime)
    # name = Column(String)
    # hostname = Column(String)
    # port = Column(String)
    # fuzzMode = Column(String)
    # fuzzcaseToExec = Column(Integer)
    # authnType = Column(String)
    # isAnonymous = Column(Boolean)
    # basicUsername = Column(String)
    # basicPassword  = Column(String)
    # bearerTokenHeader = Column(String)
    # bearerToken  = Column(String)
    # apikeyHeader  = Column(String)
    # apikey  = Column(String)
    
    def __init__(self) -> None:
        self.Id: str = ''
        self.datetime: datetime
        self.name = ''
        self.filePath = ''
        self.url = ''
        
        # execution
        self.hostname: str = ''
        self.port: int
        self.fuzzMode: FuzzMode = FuzzMode.Quick         
        self.fuzzcaseToExec = 50
        
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
        
    
    def get_fuzzcases_to_run(self):
        
        if self.fuzzExecutionConfig.fuzzMode == FuzzMode.Quick .value:
            self.fuzzExecutionConfig.fuzzcaseToExec = 50
        elif self.fuzzExecutionConfig.fuzzMode == FuzzMode.Full.value:
            self.fuzzExecutionConfig.fuzzcaseToExec = 50000
        elif self.fuzzExecutionConfig.fuzzMode == FuzzMode.Custom.value:
            if self.fuzzExecutionConfig.fuzzcaseToExec <= 0:
                self.fuzzExecutionConfig.fuzzcaseToExec = 50
                
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
    
    
    
    
