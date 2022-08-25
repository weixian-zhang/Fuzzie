from typing import Dict
from openapi3 import OpenAPI
import yaml   
from apicontext import Api, ApiContext, ApiVerb, ContentProp, ArrayItem
import requests
import validators

class OpenApi3ApiRecognizer:
    
    def load_openapi3_file(self, file_path: str):
        
        try:
            
            with open(file_path, 'r', encoding='utf-8') as f:
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
            api.parameters = self.obtain_querystring_path_parameters(apiObj.get, api)
            
            return True, api
        
        return False, None
    
    def obtain_querystring_path_parameters(self, getOperation, api: Api) -> Dict:
                
        apiParams = []
        
        params = getOperation.parameters
        
        if len(params) > 0:
            
            for param in params:
                
                name = param.name
                schema = param.schema
                type = schema.type
                api.isQueryString = True if param.in_ == "query" else False
                
                if type == 'object': 
                    
                    complexObj = []
                
                    self.get_complex_object_datatype(schema, complexObj)
                    
                    cp = ContentProp(propertyName=name, type="object", nestedContent=complexObj)
                    
                    apiParams.append(cp)
                        
                elif type ==  "array":
                    items = schema.items
                    
                    ai: ArrayItem = self.get_items_in_array_datatype(items, name)
                    
                    cp = ContentProp(propertyName=name, type=type, isArray=True, nestedContent=ai)
                    
                    apiParams.append(cp)
                        
                else:
                    apiParams.append(ContentProp(name, type))
                                     
        return apiParams
        
    
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
            
             
        
    def get_nested_content_properties(self, props, result: list):
        
        # arrayList is not None when recursing over array data type
        
        for propName in props:
            
            schema = props[propName]
            type = schema.type
            format = schema.format
            
            # complex object
            if type == "object":     #recursive case - if has more properties means nested json
                
                complexObj = []
                
                self.get_complex_object_datatype(schema, complexObj)
                
                cp = ContentProp(propertyName=propName, type="object", nestedContent=complexObj)
                
                continue
                
            else:
                #base case - primitive type
                if not type == "array":
                    
                    cp = ContentProp(propertyName=propName, type=type, format=format)
                    result.append(cp)
                    continue
                        
                if type == "array": #handles array of either complex object or primitives
                    
                    items =  schema.items # items exist for array type and is a class not iteratable
                    
                    arrayItem = self.get_items_in_array_datatype(items, propName)
                    
                    cp = ContentProp(propertyName=propName, type="array", isArray=True, nestedContent=arrayItem)
                    result.append(cp)   
    
    def get_complex_object_datatype(self, schema, result: list):
                
        # roadmap: support getting parameters from example in addition to properties
        # if properties is None:
        #     example = schema.example
        #     if not example is None:
        #         for e in example:
        #             print(e)
        
        properties = schema.properties
        
        if properties is None:
            return []
             
        for propName in properties:
            
            schema = properties[propName]
            type = schema.type
            format = schema.format
            
            if type == "object":
        
                nestedObj = []
                
                self.get_complex_object_datatype(schema, nestedObj) #recursively look for complex object
                
                cp = ContentProp(propertyName=propName, type="object", nestedContent=nestedObj)
                
                result.append(cp)
                
            elif type == "array":
                
                arrayItem = self.get_items_in_array_datatype(schema.items, propName) #recursive method
                cp = ContentProp(propertyName=propName, type="array", nestedContent=arrayItem)
                result.append(cp)
            
            # is primitive type
            else:
                cp = ContentProp(propertyName=propName, type=type, format=format)
                result.append(cp)
                                    
    # contentProp.nestedContent will be populated with new ContentProp of item in array
    def get_items_in_array_datatype(self, items, propertyName="") -> ArrayItem:
        
        # array can contain complex object,
        # calls get_complex_object_datatype to recurse if object data type exist
        #property name is used only when array is of primitive type
        
       
        if items is None:
            ai = ArrayItem(itemType="string") # default to string not such use case of item=None may not be possible
            return ai
        
        isPrimitive, itemType = self.is_array_item_primitive_type(items)

        # handles array item is of primitive type
        if isPrimitive:
            ai = ArrayItem(itemType=itemType) 
            return ai
        
        if itemType == "object":
                        
            nestedObj = []
                    
            self.get_complex_object_datatype(items, nestedObj) # items is of Schema type
            
            ai = ArrayItem(itemType=itemType, itemContent=nestedObj) 
            return ai
        
        # supports only 1 level of array item for now. [[1,2,3], [4,5,6]]
        if itemType == "array":
            
            nestedArrayItemType = None
            
            if not items.items is None: # has nested array
                nestedArrayItemType = items.items.type   
                
                if nestedArrayItemType == "array":
                    nestedArrayItemType = "string"  # defaults to string if inner array is still an array   
            else:
                nestedArrayItemType =  items.type
            
            ai = ArrayItem(itemType="array", innerArrayItemType=nestedArrayItemType) 
            return ai
                              
    
    def is_array_item_primitive_type(self, items):
        if not items.type == "object" and not items.type == "array":
            return True, items.type
        
        return False, items.type
                    
    
    def get_form_data_keyval(self, props, result):
        
        for propName in props:
            
            type = propSchema.type
            
            if type == "array":
                items = propSchema.items
                self.handleSchemaIsArray(items, dict)
            
            propSchema = props[propName]
            
            format = propSchema.format
            
            result.append(ContentProp(propName, type, format=format))
            
            
    # requestBody and content are optional in OpenApi3 for Post/Put/Patch
    # check for existence to prevent error
    def get_postputpatch_content_properties(self, postPutPatchOperation) -> list:
        
        appJsonContentType = 'application/json'
        formDataWWWFormContentType = 'application/x-www-form-urlencoded'
        multipartFormContentType = 'multipart/form-data' # single file upload, multi-files upload, or Json data + file upload
        streamFileUploadContentType = 'application/octet-stream'
        appPdfContentType = 'application/pdf'
        imagePngContentType = 'image/png'
        imageAllContentType = 'image/*'
        sameForOthersContentType = "*/*" #https://swagger.io/docs/specification/media-types/
        
        contentResult = []
        properties = None
        
        if not postPutPatchOperation.requestBody is None:
            
            if hasattr(postPutPatchOperation.requestBody, 'properties'): # $ref: '#/components/name'. Class = Schema, Assume Json
                properties = postPutPatchOperation.requestBody.properties
                self.get_nested_content_properties(properties, contentResult)
                return contentResult
            
            if hasattr(postPutPatchOperation.requestBody, 'content'): # if content exists
                
                content = postPutPatchOperation.requestBody.content
                
                # */*
                if hasattr(content, sameForOthersContentType) or self.has_attribute(content, sameForOthersContentType): 
                    sameForOthers = content[sameForOthersContentType]
                    
                    schema = sameForOthers.schema
                    
                    #TODO: test array
                    
                    #handle array params
                    if schema.type == "array":
                        self.get_items_in_array_datatype(schema.items, "")
                    else:
                        properties = sameForOthers.schema.properties
                    
                        if not properties is None:
                            self.get_form_data_keyval(properties, contentResult) #same handling as for keyval
                            
                            
                if hasattr(content, appJsonContentType) or self.has_attribute(content, appJsonContentType): 
                    jsonContent = content[appJsonContentType]
                    properties = jsonContent.schema.properties
                    
                    self.get_nested_content_properties(properties, contentResult)
                    
                if hasattr(content, formDataWWWFormContentType) or self.has_attribute(content, formDataWWWFormContentType):
                    formContent = content[formDataWWWFormContentType] 
                    properties = formContent.schema.properties
                    #self.get_form_data_keyval(properties, dictResult)
                    self.get_nested_content_properties(properties, contentResult)
                    #TODO: test array in form
                    
                    
                if hasattr(content, multipartFormContentType) or self.has_attribute(content, multipartFormContentType):
                    multipartFormContent = content[multipartFormContentType]
                    properties = multipartFormContent.schema.properties
                    self.get_nested_content_properties(properties, contentResult)
                    
                    #TODO: test array in json
                
                # assume file upload base on media type with no property name
                if (hasattr(content, streamFileUploadContentType) or self.has_attribute(content, streamFileUploadContentType) or
                    hasattr(content, appPdfContentType) or self.has_attribute(content, appPdfContentType) or
                    hasattr(content, imagePngContentType) or self.has_attribute(content, imagePngContentType) or
                    hasattr(content, imageAllContentType) or self.has_attribute(content, imageAllContentType)):
                    
                    propName = "fileupload" # fixed name for file
                    contentResult.append(ContentProp(propName, 'string', 'binary'))
                
        return contentResult
    
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
                
        
            
           
        