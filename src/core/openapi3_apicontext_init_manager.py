from pathlib import PureWindowsPath
from typing import Dict
from openapi3 import OpenAPI
import yaml   
from apicontext import Api, ApiContext, ApiVerb, RequestBodyPropertyValue


class OpenApi3ApiInitManager:
    
    def load_openapi3_file(self, file_path: str):
        
        try:
            
            with open(file_path) as f:
                spec = yaml.safe_load(f)
                
            apiContext = self.create_apicontext_from_openapi3(spec)
                             
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
            
            if not apispec.security is None:
                for authType in apispec.security:
                    apicontext.authTypes.append(authType.name)
                    
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
            api.authTypes = self.discover_api_authTypes(apiObj.get)
            api.querystring = self.get_querystring(apiObj.get)
            
            return True, api
        
        return False, None
    
    def get_querystring(self, getOperation) -> Dict:
        
        querystringParams = getOperation.parameters
        
        querystring = {}
        
        if len(querystringParams) > 0:
            
            for param in querystringParams:
                
                name = param.name
                schema = param.schema
                
                if schema.type == 'object': # nested json object
                    
                    if hasattr(schema, 'properties'):
                        nestedJsonProps = {}
                        self.get_nested_json_properties(schema.properties, nestedJsonProps)
                        querystring[name] = nestedJsonProps
                        
                else:
                    type = schema.type
                    querystring[name] = type
                    
        return querystring
        
    
    def create_post_api(self, apiObj, path):
        
        if not apiObj.post is None:
            
            api = Api()
            api.path = path
            api.verb = ApiVerb.POST
            
            api.authTypes = self.discover_api_authTypes(apiObj.post)
            
            dictBody = self.get_postputpatch_content_properties(apiObj.post)
                
            api.body = dictBody               
            
            return True, api
        
        return False, None
    
    def discover_api_authTypes(self, apiOperation):
        
        authTypes = []
        
        if hasattr(apiOperation, 'security'):
            
            security = apiOperation.security
            
            for authType in security:
                authTypes.append(authType.name)
                
        return authTypes
            
             
        
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
        streamFileUploadContentType = 'application/octet-stream'
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
                
                # aassume file upload base on media type with no property name
                if (hasattr(content, streamFileUploadContentType) or self.has_attribute(content, streamFileUploadContentType) or
                    hasattr(content, appPdfContentType) or self.has_attribute(content, appPdfContentType) or
                    hasattr(content, imagePngContentType) or self.has_attribute(content, imagePngContentType) or
                    hasattr(content, imageAllContentType) or self.has_attribute(content, imageAllContentType)):
                    dictResult['fileupload'] = RequestBodyPropertyValue('string', 'binary')
                
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
                
        
            
           
        