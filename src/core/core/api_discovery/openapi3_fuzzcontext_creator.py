
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

from apicontext import ApiContext, ParameterType, ParamProp, Api, SupportedAuthnType
from webapi_fuzzcontext import ApiFuzzCaseSet, ApiFuzzContext, FuzzMode
from eventstore import EventStore

class OpenApi3FuzzContextCreator:
    
    def __init__(self):
        self.apicontext = None
        self.fuzzcontext = ApiFuzzContext()
        self.eventstore = EventStore()
        
    def new_fuzzcontext(self,
                 apiDiscoveryMethod,  
                 isanonymous,
                 apicontext,
                 hostname, 
                 port,
                 authnType,
                 name = '',
                 requestTextContent = '',
                 requestTextFilePath = '',
                 openapi3FilePath = '',
                 openapi3Url = '',
                 openapi3Content = '',
                 fuzzcaseToExec = 100,
                 basicUsername = '',
                 basicPassword = '',
                 bearerTokenHeader = '',
                 bearerToken = '',
                 apikeyHeader = '',
                 apikey = '') -> ApiFuzzContext:
        
        fuzzcontext = ApiFuzzContext()
        fuzzcontext.Id = shortuuid.uuid()
        if name == '':
            fuzzcontext.name = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        else:
            fuzzcontext.name = name
            
        fuzzcontext.datetime = datetime.now()
        fuzzcontext.requestMessageText = requestTextContent
        fuzzcontext.requestMessageFilePath = requestTextFilePath
        fuzzcontext.openapi3FilePath = openapi3FilePath
        fuzzcontext.openapi3Content = openapi3Content
        fuzzcontext.openapi3Url = openapi3Url
        fuzzcontext.hostname = hostname
        fuzzcontext.port = port
        fuzzcontext.authnType = authnType
        fuzzcontext.fuzzcaseToExec = fuzzcaseToExec
        
        fuzzcontext.basicUsername = basicUsername
        fuzzcontext.basicPassword= basicPassword
        fuzzcontext.bearerTokenHeader= bearerTokenHeader
        fuzzcontext.bearerToken= bearerToken 
        fuzzcontext.apikeyHeader=  apikeyHeader 
        fuzzcontext.apikey= apikey
        
        fuzzcontext.authnType = self.determine_security_scheme(basicUsername,basicPassword, bearerToken, apikeyHeader,apikey)
        
        fcSets = self.create_fuzzCaseSet(apicontext)
        
        fuzzcontext.fuzzcaseSets = fcSets
        
        return fuzzcontext
        
    def create_fuzzCaseSet(self, apicontext: ApiContext) -> [ApiFuzzCaseSet]:
        
        if self.fuzzcontext  is None:
            raise Exception('initialize ApiFuzzContext with new_fuzzcontext(...)')
        
        self.set_hostname(apicontext)
        
        apis = apicontext.apis
        
        if apis == None or len(apis) == 0:
            return ApiFuzzContext()
        
        fcSets = []
        
        for api in apis:
            
            fuzzcaseSet = ApiFuzzCaseSet()
            fuzzcaseSet.Id = shortuuid.uuid()
            fuzzcaseSet.verb = api.verb.name
            
            fuzzcaseSet.path = api.path
            
            fuzzcaseSet.pathDataTemplate= self.create_path_data_template(api)
            
            querystring = self.create_querystring_data_template(api)
            fuzzcaseSet.querystringDataTemplate = querystring
            fuzzcaseSet.querystringNonTemplate = self.remove_micro_template_for_gui_display(querystring)
            
            body = self.create_body_data_template(api)
            fuzzcaseSet.bodyDataTemplate = body
            fuzzcaseSet.bodyNonTemplate = self.remove_micro_template_for_gui_display(json.dumps(body))
            
            header = self.create_header_data_template(api)
            fuzzcaseSet.headerDataTemplate = header
            fuzzcaseSet.headerNonTemplate =  self.remove_micro_template_for_gui_display(json.dumps(header))
                    
            fcSets.append(fuzzcaseSet)
            
        return fcSets
    
    def determine_security_scheme(self, 
                                  basicUsername = '',
                                  basicPassword = '',
                                  bearerToken = '', 
                                  apikeyHeader = '',
                                  apikey = '',
                                  name = '') -> str:
    
        if basicUsername != '' and basicPassword != '' and (basicUsername != 'null' and basicPassword != 'null'):
            return SupportedAuthnType.Basic.name
        elif bearerToken != '' and bearerToken != 'null':
            return SupportedAuthnType.Bearer.name
        elif apikeyHeader != '' and apikey != '' and  (apikeyHeader != 'null' and apikey != 'null'):
            return SupportedAuthnType.ApiKey.name
        else:
            return SupportedAuthnType.Anonymous.name
            
            
    
    def set_hostname(self, apicontext: ApiContext):
        
        if self.fuzzcontext.hostname == '':
            if len(apicontext.baseUrl) > 0:
                self.fuzzcontext.hostname = apicontext.baseUrl[0]
        
    
                
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
                headers[param.propertyName] = self.create_jinja_micro_template(param.type)
                  
        return headers
    
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

    
    def get_fuzzmode(self, fuzzmode: str):
        
        if fuzzmode == FuzzMode.Quick.name:
            return FuzzMode.Quick.name
        elif fuzzmode == FuzzMode.Full.name:
            return FuzzMode.Full.name
        else:
             return FuzzMode.Custom.name
        
        
        
        
    