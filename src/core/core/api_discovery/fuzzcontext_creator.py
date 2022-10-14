
# how to serialize parameters
# https://swagger.io/docs/specification/serialization/

import json
from sre_parse import fix_flags
import shortuuid
from datetime import datetime

import os,sys
from pathlib import Path
parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from apicontext import ApiContext, ParameterType, ParamProp, Api
from fuzzcontext import FuzzExecutionConfig, ApiFuzzCaseSet
from fuzzcontext import ApiFuzzContext, SecuritySchemes


class FuzzContextCreator:
    
    def __init__(self, ):
        self.apicontext = None
        self.fuzzcontext = ApiFuzzContext()
        
    def new_fuzzcontext(self,
                 name: str ,
                 hostname: str, 
                 port: int,
                 fuzzMode: str, 
                 numberOfFuzzcaseToExec: int = 50, 
                 isAnonymous = False,
                 basicAuthnUserName = '', basicAuthnPassword = '',
                 bearerTokenHeader = 'Authorization',
                 bearerToken = '', 
                 apikeyHeader = '',
                 apikey = ''):
        
        self.fuzzcontext = ApiFuzzContext()
        self.fuzzcontext.Id = shortuuid.uuid()
        if self.name == '':
            self.name = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        self.fuzzcontext.datetime = datetime.now()
        
        self.fuzzcontext.fuzzExecutionConfig = FuzzExecutionConfig()
        
        self.fuzzcontext.fuzzExecutionConfig.hostname = hostname
        self.fuzzcontext.fuzzExecutionConfig.port = port
        self.fuzzcontext.fuzzExecutionConfig.fuzzMode = fuzzMode
        self.fuzzcontext.fuzzExecutionConfig.numberOfFuzzcaseToExec = numberOfFuzzcaseToExec 
        
        #security schemes
        self.fuzzcontext.isAnonymous = isAnonymous
        self.fuzzcontext.basicUsername = basicAuthnUserName
        self.fuzzcontext.basicPassword = basicAuthnPassword
        self.fuzzcontext.bearerTokenHeader = bearerTokenHeader
        self.fuzzcontext.bearerToken = bearerToken
        self.fuzzcontext.apikeyHeader = apikeyHeader
        self.fuzzcontext.apikey = apikey
        
        #determine number of fuzz tets runs base on Quick Mode, Full Mode or Custom Mode
        self.fuzzcontext.determine_numof_fuzzcases_to_run()
        
    def create_fuzzcontext(self, apicontext: ApiContext) -> ApiFuzzContext:
        
        if self.fuzzcontext  is None:
            raise Exception('initialize ApiFuzzContext with new_fuzzcontext(...)')
        
        apis = apicontext.apis
        
        if apis == None or len(apis) == 0:
            return ApiFuzzContext()
        
        for api in apis:
            
            fuzzcaseSet = ApiFuzzCaseSet()
            fuzzcaseSet.pathDataTemplate= self.create_path_data_template(api)
            fuzzcaseSet.querystringDataTemplate = self.create_querystring_data_template(api)
            fuzzcaseSet.bodyDataTemplate = self.create_body_data_template(api)
            fuzzcaseSet.headerDataTemplate = self.create_header_data_template(api)
            fuzzcaseSet.cookieDataTemplate = self.create_cookie_data_template(api)
                    
            self.fuzzcontext.fuzzcaseSets.append(fuzzcaseSet)
            
        return self.fuzzcontext  
   
    
    # does not support array in path, array is only supported in querystring
    def create_path_data_template(self, api: Api) -> str:
        
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
    
    def create_querystring_data_template(self, api: Api) -> str:
        
        resultMap = {}
        querystring = ''
        
        if len(api.parameters) == 0:
            return querystring
        
        for param in api.parameters:
        
            if self.is_querystring_param(param.paramType):
                
                if param.type == 'object':
                    complexObject = {}
                    self.create_object_micro_data_template(param.parameters, complexObject)
                    objectJsonStr = json.dumps(complexObject)
                    querystring = querystring + f'{param.propertyName}={objectJsonStr}&' 
                    
                elif param.type == 'array':
                    arrayQSTemplate = self.create_array_data_template_for_querystring(param, 5)
                    querystring = querystring + f'{param.propertyName}={arrayQSTemplate}&'
                    
                else:
                    querystring = querystring + f'{param.propertyName}={self.create_jinja_micro_template(param.type)}&'
                    
        if len(querystring) > 0:     
            querystring = '?' + querystring
            if querystring.endswith('&'):
                querystring = querystring.rstrip(querystring[-1])
        
        return querystring
    
    # body wil be serialize to json string format
    def create_body_data_template(self, api: Api) -> str:
        
        body = {}
        
        if len(api.body) == 0:
            return body
        
        for param in api.body:
        
            if param.type == 'object':
                complexObjectDict = {}
                self.create_object_micro_data_template(param.parameters, complexObjectDict)
                body[param.propertyName] = complexObjectDict
                
            elif param.type == 'array':
                arrayOfDataTemplates = self.create_array_data_template_for_body(param, 5)
                body[param.propertyName] = arrayOfDataTemplates
            else:
                body[param.propertyName] = self.create_jinja_micro_template(param.type)
                
                
                    
        jsonBody = json.dumps(body)
        return jsonBody
    
    def create_header_data_template(self, api: Api) -> dict[str]:
        
        headers = {}
        
        if len(api.parameters) == 0:
            return headers
        
        for param in api.parameters:
            if self.is_header_param(param.paramType):
                headers[param.propertyName] = param.type
                  
        return headers
    
    def create_cookie_data_template(self, api: Api) -> dict[str]:
        
        cookies = {}
        
        if len(api.parameters) == 0:
            return cookies
        
        for param in api.parameters:
            if self.is_cookie_param(param.paramType):
                cookies[param.propertyName] = param.type
                  
        return cookies
    
    # data template helpers   
    def create_object_micro_data_template(self, parameters: list[ParamProp], resultMap: dict) -> dict:
        
        if parameters == None:
            return resultMap
        
        for param in parameters:
            
            if param.type == 'object':
                self.get_nested_parameters(param.parameters, resultMap)
                
            elif param.type == 'array':
                
                arrayQSTemplate = self.create_array_data_template_for_querystring(param, 5)
                
                resultMap[param.propertyName] = arrayQSTemplate

            else:
                resultMap[param.propertyName] = self.create_jinja_micro_template(param.type)
    
    #example: #?foo[]=bar&foo[]=qux
    #OpenApi3 does not support object
    def create_array_data_template_for_querystring(self, param: ParamProp, arraySize=5):
        
        arrayMicroTemplate = self.create_jinja_micro_template(param.arrayProp.type)
        
        propName = param.propertyName
        
        template = ''
        for x in range(arraySize):
            
            if x == arraySize - 1:
                template = template + f'{propName}[]={arrayMicroTemplate}'
            else:  
                template = template + f'{propName}[]={arrayMicroTemplate}&'
                
        return template
        
    def create_array_data_template_for_body(self, param: ParamProp, arraySize=5) -> list[str]:
        
        array = []
        arrayMicroTemplate = self.create_jinja_micro_template(param.arrayProp.type)
    
        for x in range(arraySize):
            array.append(arrayMicroTemplate)
                
        return array
                    
    
    def create_jinja_micro_template(self, type: str):
        return f'{{{{getFuzzData({type})}}}}'
    
    def is_path_param(self, paramType):
        if paramType.lower() == ParameterType.Path.value.lower():
            return True
        return False
    
    def is_querystring_param(self, paramType):
        if paramType.lower() == ParameterType.Query.value.lower():
            return True
        return False
    
    def is_header_param(self, paramType):
        if paramType.lower() == ParameterType.Header.value.lower():
            return True
        return False
    
    def is_cookie_param(self, paramType):
        if paramType.lower() == ParameterType.Cookie.value.lower():
            return True
        return False
        
        
        
        
    