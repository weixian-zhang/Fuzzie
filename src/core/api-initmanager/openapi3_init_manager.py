from typing import Dict
from openapi3 import OpenAPI
import yaml   
from apicontext import Api, ApiContext, ApiVerb, ContentPropValue
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
            api.querystring = self.obtain_get_parameters(apiObj.get, api)
            
            #handle query vs path
                #handle array as item
            
            return True, api
        
        return False, None
    
    def obtain_get_parameters(self, getOperation, api: Api) -> Dict:
        
        params = getOperation.parameters
        
        querystring = {}
        
        if len(params) > 0:
            
            for param in params:
                
                name = param.name
                schema = param.schema
                type = schema.type
                api.isQueryString = True if param.in_ == "query" else False
                
                dictParams = {}
                
                if api.isQueryString:
                    api.querystring = dictParams
                else: api.path = dictParams
                
                # nested json object
                if type == 'object': 
                    
                    if hasattr(schema, 'properties'):
                        complexObjDict = {}
                        self.get_nested_content_properties(schema.properties, complexObjDict)
                        dictParams[name] = complexObjDict
                        
                        api.querystring = querystring
                        
                elif type ==  "array":
                    items = schema.items
                    array = []
                    self.get_items_in_array_datatype(items, array, name)
                    
                    dictParams[name] = ContentPropValue(name, type, True)
                        
                else:
                    dictParams[name] = ContentPropValue(name, type)
                    
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
            
            # complex object
            if type == "object":     #recursive case - if has more properties means nested json
                
                complexObjDict = {}
                jDict[propName] = ContentPropValue(propName, type, complexObjDict)
                
                self.get_complex_object_datatype(schema.properties, complexObjDict)
                
            else:
                #base case - primitive type
                if not type == "array":
                    
                    jDict[propName]= ContentPropValue(propName, type=type, format=format)
                    continue
                        
                if type == "array": #handles array of either complex object or primitives
                    
                    items =  schema.items # items exist for array type and is a class not iteratable
                    
                    cp = ContentPropValue(propName, type="array", isArray=True)
                    jDict[propName] = cp
                    
                    contentProp = self.get_items_in_array_datatype(items, propName, contentProp=cp)        
                    
                                    
    
    def get_items_in_array_datatype(self, items, propertyName="", contentProp: ContentPropValue = None) -> ContentPropValue:
        
        # array can contain complex object,
        # calls get_complex_object_datatype to recurse if object data type exist
        #property name is used only when array is of primitive type
        
        if contentProp is None:
            raise Exception("contentProp is None for array items")
        
        if items is None:
            cp = ContentPropValue(propertyName=propertyName, type="string") # default to string not such use case of item=None may not be possible
            contentProp.nestedObjectsContent = cp
        
        isPrimitive, itemType = self.is_array_item_primitive_type(items)

        # handles array item is of primitive type
        if isPrimitive:
            contentProp.arrayItemType = itemType       
        
        if itemType == "object":
            
            # TODO: should complexObj be dict or content prop
            
            complexObjDict = {}
            
            cp = ContentPropValue(propertyName, itemType, complexObjDict)
            
            contentProp.nestedObjectsContent = cp
                    
            self.get_complex_object_datatype(items.properties, complexObjDict) 
        
        # supports only 1 level of array item for now. [[1,2,3], [4,5,6]]
        if itemType == "array":
            
            if not items.items is None: # has nested array
                contentProp = ContentPropValue(propertyName, type="array", isArray=True)
            
            
            pass
            
            #if not items.items is None:
                
            
        
                    
        # for propName in properties: # complex object in array
            
        #     schema = properties[propName]
        #     type = schema.type
            
        #     if type == "object": # complex object
                
        #         complexObjDict = {}
        #         complexObjDict[propName] = ContentPropValue(propName, type, complexObjDict)
                
        #         self.get_complex_object_datatype(schema.properties, complexObjDict) #recurse complex object
                
        #         continue # prevent adding duplicate prop:val
            
        #     if type == "array": # nested array
                
        #         isPrimitive, arrayValType = self.is_array_item_primitive_type(schema.items)
            
        #         if isPrimitive:
        #             arrayResult.append(ContentPropValue(propName, arrayValType, isArray=True))
        #             continue
                
        #         s
                
        #     else:
        #         arrayResult.append(ContentPropValue(propName, type))
                
                
    def get_complex_object_datatype(self, properties, dictResult):
        
        for propName in properties:
            
            schema = properties[propName]
            type = schema.type
            format = schema.format
            
            if type == "object":
        
                complexObj = {}
                contentProp = ContentPropValue(propertyName=propName, type=type, nestedObjectsContent=complexObj)
                dictResult[propName] = contentProp
                
                self.get_complex_object_datatype(schema.properties, complexObj)
                
            elif type == "array":
                
                contentProp = self.get_items_in_array_datatype(schema.items, propName) #recursive method
                dictResult[propName] = contentProp
                
            else:
                dictResult[propName]= ContentPropValue(propName, type, format=format)
    
    def is_array_item_primitive_type(self, items):
        if not items.type == "object" and "array":
            return True, items.type
        
        return False, items.type
                    
    
    def get_form_data_keyval(self, props, dict):
        
        for propName in props:
            
            type = propSchema.type
            
            if type == "array":
                items = propSchema.items
                self.handleSchemaIsArray(items, dict)
            
            propSchema = props[propName]
            
            
            format = propSchema.format
            
            dict[propName]= ContentPropValue(propName, type, format=format)
            
            
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
                    dictResult[propName] = ContentPropValue(propName, 'string', 'binary')
                
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
                
        
            
           
        