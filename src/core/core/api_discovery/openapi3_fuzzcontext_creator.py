
# how to serialize parameters
# https://swagger.io/docs/specification/serialization/

import json
from sre_parse import fix_flags
import shortuuid
from datetime import datetime

import os,sys
from pathlib import Path

parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from apicontext import ApiContext, ParameterType, ParamProp, Api
from fuzzcontext import ApiFuzzCaseSet, ApiFuzzContext, FuzzMode
from eventstore import EventStore

class OpenApi3FuzzContextCreator:
    
    def __init__(self, eventstore: EventStore):
        self.apicontext = None
        self.fuzzcontext = ApiFuzzContext()
        self.eventstore = eventstore
        
    def new_fuzzcontext(self,
                 hostname: str, 
                 port: int,
                 fuzzMode: str, 
                 numberOfFuzzcaseToExec: int = 50, 
                 isAnonymous = False,
                 basicUsername = '',
                 basicPassword = '',
                 bearerTokenHeader = 'Authorization',
                 bearerToken = '', 
                 apikeyHeader = '',
                 apikey = '',
                 name = '',
                 filePath = '',
                 url = ''):
        
        self.fuzzcontext = ApiFuzzContext()
        self.fuzzcontext.Id = shortuuid.uuid()
        if self.fuzzcontext.name == '':
            self.fuzzcontext.name = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        else:
            self.fuzzcontext.name = name
            
        self.fuzzcontext.datetime = datetime.now()
        
        if fuzzMode == FuzzMode.Quick.name:
            self.fuzzcontext.fuzzMode = FuzzMode.Quick
        elif fuzzMode == FuzzMode.Full.name:
            self.fuzzcontext.fuzzMode = FuzzMode.Full
        else:
             self.fuzzcontext.fuzzMode = FuzzMode.Custom
        
        self.fuzzcontext.filePath = filePath
        self.fuzzcontext.url = url
        self.fuzzcontext.hostname = hostname
        self.fuzzcontext.port = port
        self.fuzzcontext.numberOfFuzzcaseToExec = numberOfFuzzcaseToExec 
        
        #security schemes
        self.fuzzcontext.isAnonymous = isAnonymous
        self.fuzzcontext.basicUsername = basicUsername
        self.fuzzcontext.basicPassword = basicPassword
        self.fuzzcontext.bearerTokenHeader = bearerTokenHeader
        self.fuzzcontext.bearerToken = bearerToken
        self.fuzzcontext.apikeyHeader = apikeyHeader
        self.fuzzcontext.apikey = apikey
        
    def create_fuzzcontext(self, apicontext: ApiContext) -> ApiFuzzContext:
        
        if self.fuzzcontext  is None:
            raise Exception('initialize ApiFuzzContext with new_fuzzcontext(...)')
        
        apis = apicontext.apis
        
        if apis == None or len(apis) == 0:
            return ApiFuzzContext()
        
        for api in apis:
            
            fuzzcaseSet = ApiFuzzCaseSet()
            fuzzcaseSet.Id = shortuuid.uuid()
            fuzzcaseSet.verb = api.verb
            
            fuzzcaseSet.path = api.path
            
            fuzzcaseSet.pathDataTemplate= self.create_path_data_template(api)
            
            querystring = self.create_querystring_data_template(api)
            fuzzcaseSet.querystringDataTemplate = querystring
            fuzzcaseSet.querystringNonTemplate = self.remove_micro_template_for_gui_display(querystring)
            
            body = self.create_body_data_template(api)
            fuzzcaseSet.bodyDataTemplate = body
            fuzzcaseSet.bodyNonTemplate = self.remove_micro_template_for_gui_display(json.dumps(body))
            
            fuzzcaseSet.headerDataTemplate = self.create_header_data_template(api)
            fuzzcaseSet.cookieDataTemplate = self.create_cookie_data_template(api)
                    
            self.fuzzcontext.fuzzcaseSets.append(fuzzcaseSet)
            
        return self.fuzzcontext  
   
    def remove_micro_template_for_gui_display(self, datatemplate: str):
       if datatemplate == '':
            return datatemplate
        
       datatemplate = datatemplate.replace('{{getFuzzData(', '')
       datatemplate = datatemplate.replace(')}}', '')
       return datatemplate
    
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
    
        qsDT = ''       
        
        if len(api.parameters) == 0:
            return qsDT
        
        for param in api.parameters:
        
            if self.is_querystring_param(param.paramType):
                
                if param.type == 'object':
                    complexObject = {}
                    self.create_object_micro_data_template(param.parameters, complexObject)
                    objectJsonStr = json.dumps(complexObject)
                    qsDT = qsDT + f'{param.propertyName}={objectJsonStr}&'
                    
                elif param.type == 'array':
                    arrayQSTemplate = self.create_array_data_template_for_querystring(param, 5)
                    qsDT = qsDT + f'{param.propertyName}={arrayQSTemplate}&'
                    
                else:
                    qsDT = qsDT + f'{param.propertyName}={self.create_jinja_micro_template(param.type)}&'

                    
        if len(qsDT) > 0:     
            qsDT = '?' + qsDT
            if qsDT.endswith('&'):
                qsDT = qsDT.rstrip(qsDT[-1])
            
        return qsDT
    
    # body wil be serialize to json string format
    def create_body_data_template(self, api: Api)  -> dict[str]:
        
        #bodyNonTemplate = {}
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


        return body
    
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
        
        
        
        
    