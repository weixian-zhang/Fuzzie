
# how to serialize parameters
# https://swagger.io/docs/specification/serialization/

import json
from sre_parse import fix_flags
from apicontext_model import ApiContext, ApiVerb, ParameterType, ParamProp, Api, ArrayItem
from api_discovery.fuzzcontext_model import FuzzExecutionConfig, ApiFuzzCaseSet
from fuzzcontext_model import ApiFuzzContext, FuzzMode, SecuritySchemes
import json

class FuzzContextCreator:
    
    def __init__(self):
        self.apicontext = None
        self.fuzzcontext = ApiFuzzContext()
        
    def set_fuzzExecutionConfig(self,
                 hostname: str, 
                 port: int,
                 fuzzMode: str, 
                 numberOfFuzzcaseToExec: int = 50, 
                 isAnonymous = False,
                 basicAuthnUserName = '', basicAuthnPassword = '',
                 bearerTokenHeaderName = 'Authorization',
                 bearerToken = '', 
                 apikeyAuthnHeaderName = '',
                 apikeyAuthnKey = ''):
        
        self.fuzzcontext.fuzzExecutionConfig = FuzzExecutionConfig()
        
        self.fuzzcontext.fuzzExecutionConfig.hostname = hostname
        self.fuzzcontext.fuzzExecutionConfig.port = port
        self.fuzzcontext.fuzzExecutionConfig.fuzzMode = fuzzMode
        self.fuzzcontext.fuzzExecutionConfig.numberOfFuzzcaseToExec = numberOfFuzzcaseToExec 
        
        #security schemes
        self.fuzzcontext.fuzzExecutionConfig.securitySchemes = SecuritySchemes()
        self.fuzzcontext.fuzzExecutionConfig.securitySchemes.basicAuthnUserName = basicAuthnUserName
        self.fuzzcontext.fuzzExecutionConfig.securitySchemes.basicAuthnPassword = basicAuthnPassword
        self.fuzzcontext.fuzzExecutionConfig.securitySchemes.bearerTokenHeaderName = bearerTokenHeaderName
        self.fuzzcontext.fuzzExecutionConfig.securitySchemes.bearerToken = bearerToken
        self.fuzzcontext.fuzzExecutionConfig.securitySchemes.apikeyAuthnHeaderName = apikeyAuthnHeaderName
        self.fuzzcontext.fuzzExecutionConfig.securitySchemes.apikeyAuthnKey = apikeyAuthnKey
        
        #determine number of fuzz tets runs base on Quick Mode, Full Mode or Custom Mode
        self.fuzzcontext.determine_numof_fuzzcases_to_run()
        
    def create_fuzzcontext(self, apicontext: ApiContext) -> ApiFuzzContext:
        
        apis = apicontext.apis
        
        if apis == None or len(apis) == 0:
            return ApiFuzzContext()
        
        fuzzcaseSet = ApiFuzzCaseSet()
        
        for api in apis:
            
            fuzzcaseSet.pathDataTemplate= self.create_path_data_template(api)
            
            self.fuzzcontext.fuzzcaseSets.append(fuzzcaseSet)
            
        return self.fuzzcontext
                
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
    
   
    
    # does not support array in path, array is supported only in querystring
    def create_path_data_template(self, api: Api) -> dict:
        
        resultMap = {}
        
        if len(api.parameters) == 0:
            return api.path
        
        for param in api.parameters:
        
            if self.is_path_param(param.paramType):
                
                if param.type == 'object':
                    resultMap[param.propertyName] = self.create_object_micro_data_template(param.parameters, resultMap)
                    
                else:
                    resultMap[param.propertyName] = self.create_jinja_micro_template(param.type)
                    
        if len(resultMap) > 0:     
            apiPathDataTemplate = api.path.format_map(resultMap)
            return apiPathDataTemplate
        
        return api.path
    
    def create_querystring_data_template(self, api: Api):
                        # elif param.type == 'array':
                #     microTemplate = self.create_array_micro_data_template(param)
                
                #     arrayQSTemplate = self.create_querystring_array_data_template(param, microTemplate, 5)
                    
                #     resultMap[param.propertyName] = arrayQSTemplate
        pass
                
    def create_object_micro_data_template(self, parameters: list[ParamProp], resultMap: dict) -> dict:
        
        if parameters == None:
            return resultMap
        
        for param in parameters:
            
            if param.type == 'object':
                self.get_nested_parameters(param.parameters, resultMap)
                
            elif param.type == 'array':
                
                microTemplate = self.create_array_micro_data_template(param)
                
                arrayQSTemplate = self.create_querystring_array_data_template(param, microTemplate, 5)
                
                resultMap[param.propertyName] = arrayQSTemplate

            else:
                resultMap[param.propertyName] = self.create_jinja_micro_template(param.type)
    
    #example: #?foo[]=bar&foo[]=qux 
    def create_querystring_array_data_template(self, param: ParamProp, microTemplate: str, arraySize=5):
        propName = param.propertyName
        
        template = f'?'
        for x in range(arraySize):
            
            if x == arraySize - 1:
                template = template + f'{propName}[]={microTemplate}'
            else:  
                template = template + f'{propName}[]={microTemplate}&'
                
        return template
        
        
    
    def create_body_array_data_template(microTemplate: str, arraySize=5):
        pass
    
    # following OpenAPI3 standard, array item only supports primitive type, object is not supported.
    def create_array_micro_data_template(self, param: ParamProp):
        
        dataTemplate = self.create_jinja_micro_template(param.arrayProp.type)
        # if param.arrayProp.type == 'object':
                    
        #     arrayComplexObj = {}
        #     self.get_nested_parameters(param.arrayProp.parameters, arrayComplexObj)
        #     dataTemplate = json.dumps(arrayComplexObj)
        # else:   
        #     dataTemplate = self.create_jinja_micro_template(param.arrayProp.type)
            
        return dataTemplate
                
    
    def create_jinja_micro_template(self, type: str):
        return f'{{{{ getFuzzData({type}) }}}}'
    
    def is_path_param(self, paramType):
        
        if paramType.lower() == ParameterType.Path.value.lower():
            return True
        return False
    
    def is_param_array(paramType: str) -> bool:
        
        if paramType.startswith('array:'):
            arrayType = paramType.split(':')[0]
            return True, arrayType
        
        return False, ''
        
        
        
        
    