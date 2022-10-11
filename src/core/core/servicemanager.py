from api_discovery.apicontext_model import ApiContext
from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.fuzzcontext_creator import FuzzContextCreator
from api_discovery.fuzzcontext_model import FuzzExecutionConfig, FuzzMode
from api_discovery.fuzzcontext_model import ApiFuzzCaseSet, ApiFuzzContext
from eventstore import EventStore

class ServiceManager:
    
    def __init__(self,
                 eventstore: EventStore) -> None:
        
        self.fuzzContext: None
        
        self.eventstore = eventstore
        
        self.fuzzcontextCreator = FuzzContextCreator()
        
    def set_fuzzExecConfig(self,
                 hostname: str, 
                 port: int, 
                 fuzzMode: str = FuzzMode.Quick.value, 
                 numberOfFuzzcaseToExec: int = 50, 
                 isAnonymous = False,
                 basicAuthnUserName = '', 
                 basicAuthnPassword = '',
                 bearerTokenHeaderName = '',
                 bearerToken = '', 
                 apikeyAuthnHeaderName = '',
                 apikeyAuthnKey = ''):
        
        self.fuzzcontextCreator.set_fuzzExecutionConfig(hostname=hostname,
                                                        port=port,
                                                        fuzzMode=fuzzMode,
                                                        numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                                                        isAnonymous=isAnonymous,
                                                        basicAuthnUserName=basicAuthnUserName,
                                                        basicAuthnPassword=basicAuthnPassword,
                                                        bearerTokenHeaderName=bearerTokenHeaderName,
                                                        bearerToken=bearerToken,
                                                        apikeyAuthnHeaderName=apikeyAuthnHeaderName,
                                                        apikeyAuthnKey=apikeyAuthnKey)
        
    
    def create_fuzzcontext_from_openapi3_spec_file(self, filePath):
        
        openapi3Loader = OpenApi3ApiDiscover(self.eventstore)
        apicontext = openapi3Loader.load_openapi3_file(filePath)
        
        fuzzContext = self.fuzzcontextCreator.create_fuzzcontext(apicontext)
        
        # def getFuzzData(self,type):
        #     return '1231'
        # from jinja2 import Template
        # tm = Template(fuzzContext.fuzzcaseSets[0].pathDataTemplate)
        # path = tm.render(getFuzzData=getFuzzData)
        # print(path)
        
        return fuzzContext
    
    
        
    
    def create_fuzzcontext_from_openapi3_url(self, url):
        pass
    
    def load_existing_fuzzcontext(fuzzcontextId: str):
        #load from db.py
        pass
    