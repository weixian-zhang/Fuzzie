from typing import Dict
from openapi3 import OpenAPI
import yaml   
from apicontext import Api, ApiContext, ApiVerb, ReqBodyContentPropValue
import requests
import validators

class OpenApi3ApiInitManager:
    
    def load_openapi3_file(self, file_path: str):
        
        try:
            
            with open(file_path) as f:
                spec = yaml.safe_load(f)
                
            apiContext = self.create_apicontext_from_openapi3(spec)
            
            return apiContext
                             
        except Exception as e:
            print(e)
            raise
        
    def load_openapi3_url(self, url: str):
        
        if not validators.url(url):
            raise Exception('Url is malformed')
        
        resp = requests.get(url)
        specStr = resp.text
        spec = yaml.safe_load(specStr)
                
        apiContext = self.create_apicontext_from_openapi3(spec)
        
        return apiContext
            
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
            
            #handle query vs path
                #handle array as item
            
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
                        self.get_nested_content_properties(schema.properties, nestedJsonProps)
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
            
             
        
    def get_nested_content_properties(self, props, jDict):
        
        # arrayList is not None when recursing over array data type
        
        for propName in props:
            
            schema = props[propName]
            type = schema.type
            format = schema.format
            
            if type == "object":     #recursive case - if has more properties means nested json
                
                newJDict = {}
                jDict[propName] = newJDict
                
                self.get_contentprops_complex_object_datatype(schema.properties, newJDict)
                
            else:
                #base case
                if not type == "array":
                    
                    jDict[propName]= ReqBodyContentPropValue(propName, type, format=format)
                    continue
                        
                if type == "array": #handles array of either complex object or primitives
                    
                    arrayResult = []
                    
                    jDict[propName] = arrayResult
                    
                    items =  schema.items # items exist for array type and is a class not iteratable
                    
                    self.get_contentprops_array_datatype(items, arrayResult, propName)
                                    
    
    def get_contentprops_array_datatype(self, items, arrayResult: list, propertyName=""):
        
        #array may contain complex object,
        # calls get_contentprops_complex_object_datatype to recurse if object data type exist
        #property name is used only when array is of primitive type
        
        if items is None:
            return []
        
        properties = items.properties
        
        if properties is None: # array contains primitive type only
            isPrimitive, arrayValType = self.is_array_datatype_of_primitive_value(items)
            
            if isPrimitive:
                arrayResult.append(ReqBodyContentPropValue(propertyName, arrayValType, isArray=True))
                return arrayResult
            else:
                return [] # should not be the case until use case is found
                    
        for propName in properties: # compelx object in array
            
            schema = properties[propName]
            type = schema.type
            
            if type == "object": # 
                
                newJDict = {}
                arrayResult.append(newJDict)
                self.get_contentprops_complex_object_datatype(schema.properties, newJDict) #recurse complex object
                continue # prevent adding duplicate prop:val
            
            if type == "array": # nested array
                
                isPrimitive, arrayValType = self.is_array_datatype_of_primitive_value(schema.items)
            
                if isPrimitive:
                    arrayResult.append(ReqBodyContentPropValue(propName, arrayValType, isArray=True))
                    continue
                
                nestedArray = []
                arrayResult.append(nestedArray)
                self.get_contentprops_array_datatype(schema.items, nestedArray)
                
            else:
                arrayResult.append(ReqBodyContentPropValue(propName, type))
                
                
    def get_contentprops_complex_object_datatype(self, properties, dictResult):
        
        for propName in properties:
            
            schema = properties[propName]
            type = schema.type
            format = schema.format
            
            if type == "object":
        
                newJDict = {}
                dictResult[propName] = newJDict
                
                self.get_contentprops_complex_object_datatype(schema.properties, newJDict)
            else:
                dictResult[propName]= ReqBodyContentPropValue(propName, type, format=format)
                
    def is_array_datatype_of_primitive_value(self, schemaItems):
        
        arrayValType = schemaItems.type
        
        if arrayValType == "object":
            return False, arrayValType
        
        return True, arrayValType
                
    
    def get_form_data_keyval(self, props, dict):
        
        for propName in props:
            
            type = propSchema.type
            
            if type == "array":
                items = propSchema.items
                self.handleSchemaIsArray(items, dict)
            
            propSchema = props[propName]
            
            
            format = propSchema.format
            
            dict[propName]= ReqBodyContentPropValue(propName, type, format=format)
            
            
    # requestBody and content are optional in OpenApi3 for Post/Put/Patch
    # check for existence to prevent error
    def get_postputpatch_content_properties(self, postPutPatchOperation) -> Dict:
        
        appJsonContentType = 'application/json'
        formDataWWWFormContentType = 'application/x-www-form-urlencoded'
        multipartFormContentType = 'multipart/form-data' # single file upload, multi-files upload, or Json data + file upload
        streamFileUploadContentType = 'application/octet-stream'
        appPdfContentType = 'application/pdf'
        imagePngContentType = 'image/png'
        imageAllContentType = 'image/*'
        sameForOthersContentType = "*/*" #https://swagger.io/docs/specification/media-types/
        
        dictResult = {}
        properties = None
        
        if not postPutPatchOperation.requestBody is None:
            
            if hasattr(postPutPatchOperation.requestBody, 'properties'): # $ref: '#/components/name'. Class = Schema, Assume Json
                properties = postPutPatchOperation.requestBody.properties
                self.get_nested_content_properties(properties, dictResult)
                return dictResult
            
            if hasattr(postPutPatchOperation.requestBody, 'content'): # if content exists
                
                content = postPutPatchOperation.requestBody.content
                
                if hasattr(content, sameForOthersContentType) or self.has_attribute(content, sameForOthersContentType): 
                    sameForOthers = content[sameForOthersContentType]
                    
                    schema = sameForOthers.schema
                    
                    #TODO: test array
                    
                    #handle array params
                    if schema.type == "array":
                        self.handleSchemaIsArray(schema.items, dictResult)
                    else:
                        properties = sameForOthers.schema.properties
                    
                        if not properties is None:
                            self.get_form_data_keyval(properties, dictResult) #same handling as for keyval
                            
                            
                if hasattr(content, appJsonContentType) or self.has_attribute(content, appJsonContentType): 
                    jsonContent = content[appJsonContentType]
                    properties = jsonContent.schema.properties
                    
                    self.get_nested_content_properties(properties, dictResult)
                    
                if hasattr(content, formDataWWWFormContentType) or self.has_attribute(content, formDataWWWFormContentType):
                    formContent = content[formDataWWWFormContentType] 
                    properties = formContent.schema.properties
                    #self.get_form_data_keyval(properties, dictResult)
                    self.get_nested_content_properties(properties, dictResult)
                    #TODO: test array in form
                    
                    
                if hasattr(content, multipartFormContentType) or self.has_attribute(content, multipartFormContentType):
                    multipartFormContent = content[multipartFormContentType]
                    properties = multipartFormContent.schema.properties
                    self.get_nested_content_properties(properties, dictResult)
                    
                    #TODO: test array in json
                
                # aassume file upload base on media type with no property name
                if (hasattr(content, streamFileUploadContentType) or self.has_attribute(content, streamFileUploadContentType) or
                    hasattr(content, appPdfContentType) or self.has_attribute(content, appPdfContentType) or
                    hasattr(content, imagePngContentType) or self.has_attribute(content, imagePngContentType) or
                    hasattr(content, imageAllContentType) or self.has_attribute(content, imageAllContentType)):
                    
                    propName = "fileupload" # fixed name for file
                    dictResult[propName] = ReqBodyContentPropValue(propName, 'string', 'binary')
                
        return dictResult
    
    def handleSchemaIsArray(self, items, dictResult):
        
        if not items is None: 
                                        
            if not items.properties is None: # if properties is not None, is array of complex object
                
                self.get_form_data_keyval(items.properties, dictResult)
                return dictResult
            
            else:
                dictResult["array"] = items.type #array of primitive tpye            
    
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
                
        
            
           
        