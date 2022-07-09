from pathlib import PureWindowsPath
from typing import Dict
from openapi3 import OpenAPI
import yaml   
import enum

class ApiVerb(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5

class RequestBodyPropertyValue:
    type: str = ''
    format: str = None
    
    def __init__(self, type, format) -> None:
        self.type = type
        self.format = format
        
    def is_file_upload() -> bool:
        if type == 'string' and (format == 'binary' or format == 'base64'):
            return True
        return False
    
class ApiContext:
    
    baseUrl = []
    title: str = ''
    version: str = ''
    apis = []

class Api:
    
    path: str = '' #path includes querystring
    operationId: str = ''
    verb: ApiVerb = ApiVerb.GET
    body = {}    

class ApiInitManager:
    
    def load_openapi3_yaml_file(self, file_path: str):
        
        try:
            
            with open(file_path) as f:
                specYaml = yaml.safe_load(f)
                
            apiContext = self.create_apicontext_from_openapi3(specYaml)
                             
        except Exception as e:
            print(e)
            
            
    def create_apicontext_from_openapi3(self, openapiYaml) -> ApiContext:
        
        try:
            
            apispec = OpenAPI(openapiYaml)
            
            apicontext = ApiContext()
            
            apicontext.title = apispec.info.title
            apicontext.version = apispec.info.version
            
            #server info
            if not apispec.servers is None:
                for server in apispec.servers:
                    apicontext.baseUrl.append(server.url)
                    
            # paths
            if not apispec.paths is None:
                for pathStr in apispec.paths:
                    
                  apiObj =  apispec.paths[pathStr]
                  
                  hasGet, getApi = self.create_get_api(apiObj, pathStr)
                  if hasGet:
                      apicontext.apis.append(getApi)
                  
                  hasPost, postApi = self.create_post_api(apiObj, pathStr)
                  if hasPost:
                      apicontext.apis.append(postApi)
                    
            return apicontext
        
        except Exception as e:
            print(e)
            raise
        
    def create_get_api(self, apiObj, path):
        
        if not apiObj.get is None:
            api = Api()
            if not apiObj.get.operationId is None:
                api.operationId = apiObj.get.operationId
            api.path = path
            api.verb = ApiVerb.GET
            
            return True, api
        
        return False, None
    
    def create_post_api(self, apiObj, path):
        
        #https://swagger.io/docs/specification/describing-request-body/
        #understand request-body structure, example/examples are part of spec
        #https://github.com/Dorthu/openapi3/blob/master/tests/ref_test.py
        
        #file upload
        # https://stackoverflow.com/questions/14455408/how-to-post-files-in-swagger-openapi
        # https://swagger.io/docs/specification/describing-request-body/file-upload/
        
        if not apiObj.post is None:
            
            api = Api()
            api.path = path
            api.verb = ApiVerb.POST
            
            dictBody = self.get_postputpatch_content_properties(apiObj.post)
                
            api.body = dictBody               
            
            return True, api
        
        return False, None        
        
    def get_nested_json_properties(self, props, jDict):
        
        for propName in props:
            
            propSchema = props[propName]
            type = propSchema.type
            format = propSchema.format
            
            #recurs case - if has more properties means nested json
            if type == 'object':
                
                newJDict = {}
                
                jDict[propName] = newJDict
                
                self.get_nested_json_properties(propSchema.properties, newJDict)
            else:
                #base case
                jDict[propName]= RequestBodyPropertyValue(type, format)
                
    
    def get_form_data_keyval(self, props, dict):
        
        for propName in props:
            
            propSchema = props[propName]
            
            type = propSchema.type
            format = propSchema.format
            
            dict[propName]= RequestBodyPropertyValue(type, format)
            
            
    # requestBody and content are optional in OpenApi3 for Post/Put/Patch
    # check for existence to prevent error
    def get_postputpatch_content_properties(self, postPutPatchOperation) -> Dict:
        
        appJsonContentType = 'application/json'
        formDataWWWFormContentType = 'application/x-www-form-urlencoded'
        multipartFormContentType = 'multipart/form-data' # single file or form + file or multiple files without form data
        appPdfContentType = 'application/pdf'
        imagePngContentType = 'image/png'
        imageAllContentType = 'image/*'
        
        dictResult = {}
        properties = None
        
        if not postPutPatchOperation.requestBody is None:
            
            if hasattr(postPutPatchOperation.requestBody, 'properties'): # $ref: '#/components/name'. Class = Schema, Assume Json
                properties = postPutPatchOperation.requestBody.properties
                self.get_nested_json_properties(properties, dictResult)
                return dictResult
            
            if hasattr(postPutPatchOperation.requestBody, 'content'): # if content exists
                
                content = postPutPatchOperation.requestBody.content
                
                if hasattr(content, appJsonContentType) or self.has_attribute(content, appJsonContentType): 
                    jsonContent = content[appJsonContentType]
                    properties = jsonContent.schema.properties
                    
                    self.get_nested_json_properties(properties, dictResult)
                    
                if hasattr(content, formDataWWWFormContentType) or self.has_attribute(content, formDataWWWFormContentType):
                    formContent = content[formDataWWWFormContentType] 
                    properties = formContent.schema.properties
                    self.get_form_data_keyval(properties, dictResult)
                    
                if hasattr(content, multipartFormContentType) or self.has_attribute(content, multipartFormContentType):
                    multipartFormContent = content[multipartFormContentType]
                    properties = multipartFormContent.schema.properties
                    self.get_nested_json_properties(properties, dictResult)
                
        return dictResult
    
    def get_postputpatch_content_props(self, content):
        
        props = None
        
        if hasattr(content, 'schema'):
             if hasattr(content, 'properties'):
                props = content.schema.properties
        
        if hasattr(content, 'properties'): # $ref: '#/components/name'
            props = content.properties
            
        return props
    
    def has_attribute(self, obj, attrName):
        
        for k in obj:
            if k == attrName:
                return True
        
        return False
                
        
            
           
        