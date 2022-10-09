
# how to serialize parameters
# https://swagger.io/docs/specification/serialization/

from sre_parse import fix_flags
from apicontext_model import ApiContext, GetApi, MutatorApi, ApiVerb
from fuzzcontext_model import ApiFuzzContext, FuzzMode, GetApiFuzzCaseSet

class FuzzContextCreator:
    
    def __init__(self, hostname: str, port: int, fuzzMode: str, 
                 fuzzcaseToExec, apicontext: ApiContext,
                 basicAuthnUserName = '', basicAuthnPassword = '',
                 bearerTokenHeaderName = 'Authorization',
                 bearerToken = '', 
                 apikeyAuthnHeaderName = '',
                 apikeyAuthnKey = ''):
        
        self.hostname = hostname
        self.port = port
        self.fuzzMode = fuzzMode
        self.fuzzcaseToExec = fuzzcaseToExec 
        self.apicontext = apicontext
        
        #security schemes
        self.basicAuthnUserName = basicAuthnUserName
        self.basicAuthnPassword = basicAuthnPassword
        self.bearerTokenHeaderName = bearerTokenHeaderName
        self.bearerToken = bearerToken
        self.apikeyAuthnHeaderName = apikeyAuthnHeaderName
        self.apikeyAuthnKey = apikeyAuthnKey
        
    def create_fuzzcontext(self):
        
        apis = self.apicontext.apis
        
        if apis == None or len(apis) == 0:
            return ApiFuzzContext()
        
        
        
        for api in apis:
            
            if self.isGet(api.verb):
                
                getApi: GetApi  = api
                
                fuzzcaseSet = self.create_get_ApiFuzzCaseSet(getApi)
                
            
                
                
    def isGet(self, verb):
        if verb.lower() == ApiVerb.GET.value.lower():
            return True
        return False
    
    def isMutator(self, verb):
        if (verb.lower() == ApiVerb.POST.value.lower() or
            verb.lower() == ApiVerb.PATCH.value.lower() or
            verb.lower() == ApiVerb.DELETE.value.lower() or
            verb.lower() == ApiVerb.PUT.lower()):
            return True
        return False
    
    def create_fuzzcontext(self, apicontext: ApiContext):
        pass
    
    def create_get_ApiFuzzCaseSet(self, getapi: GetApi) -> GetApiFuzzCaseSet:
        
        fuzzcaseSet = GetApiFuzzCaseSet()
        
        fuzzcaseSet.selected = False
        
        
        
        
        
        
    