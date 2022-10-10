from api_discovery.apicontext_model import ApiContext
from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.fuzzcontext_creator import FuzzContextCreator
from api_discovery.fuzzcontext_model import FuzzExecutionConfig, FuzzMode
from api_discovery.fuzzcontext_model import ApiFuzzCaseSet, ApiFuzzContext
from eventstore import EventStore

class FuzzManager:
    
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
        
    
    def create_fuzz_context_from_openapi3_spec_file(self, filePath):
        
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
    
    
        
    
    def create_fuzz_context_from_openapi3_url(self, url):
        pass
    
    def load_existing_fuzzcontext(fuzzcontextId: str):
        #load from db.py
        pass
    
    
    
    
    # def fuzz(self, json):
        
    #     print(f'In DefaultFuzzer, discover API schema with OpenApi3 Url: {self.openapiUrl}')
        
    #     openapiUrl = json["openapiUrl"]
    #     openapiFilePath = json["openapiFilePath"]
    #     openapiFilePath = json["openapiFilePath"]
    #     requestTextFilePath = json["requestTextFilePath"]
    #     requestTextSingle = json["requestTextSingle"]
    #     workingDirectory = json["workingDirectory"]
        
    #     if not openapiUrl == "" and not validators.url(openapiUrl):
    #         print("Invalid OpenApi Url")
    #         return
        
        
    #     self.fuzzContext = ApiFuzzContext(openapiUrl, openapiFilePath, requestTextFilePath, requestTextSingle, workingDirectory)
    
        #TODO

        # API schema source from client
            # openapi3 url
            # openapi3 file path
            # .fuzzie file path - that describes api schema 
            # textual api string
            
            # create ApiContext from api source
            
            # fuzzing - 
            
            
        # call data factory prepare data
        
        #fuzzing
        
        #update progress