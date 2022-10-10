from typing import Dict
from openapi3 import OpenAPI
import yaml   
from apicontext_model import Api, ApiContext, ApiVerb, ParamProp, ArrayItem
import requests
import validators

import os,sys
from pathlib import Path
parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
from eventstore import EventStore

class OpenApi3ApiDiscover:
    
    def __init__(self, eventstore: EventStore) -> None:
        self.eventstore = eventstore
    
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
                                
            # paths
            if not apispec.paths is None:
                for pathStr in apispec.paths:
                    
                  apiObj =  apispec.paths[pathStr]
                  
                  hasGet, getApi = self.create_get_api(apiObj, pathStr)
                  if hasGet:
                      apicontext.apis.append(getApi)
                  
                  hasPost, postApi = self.create_mutator_api(apiObj, pathStr)
                  if hasPost:
                      apicontext.apis.append(postApi)
                    
            return apicontext
        
        except Exception as e:
            self.eventstore.emitErr(e)
            raise
        
        
    def create_get_api(self, apiObj, path):
        
        if not apiObj.get is None:
            api = Api()
            if not apiObj.get.operationId is None:
                api.operationId = apiObj.get.operationId
            api.path = path
            api.verb = ApiVerb.GET
            api.parameters = self.obtain_parameters(apiObj.get)
                        
            return True, api
        
        return False, None        
        
    def obtain_parameters(self, operation) -> Dict:
                
        apiParams = []
        
        params = operation.parameters
        
        if len(params) > 0:
            
            for param in params:
                
                name = param.name
                schema = param.schema
                type = schema.type
                
                if type == 'object': 
                    
                    complexObj = []
                
                    self.get_complex_object_datatype(schema, complexObj)
                    
                    cp = ParamProp(propertyName=name, type="object", parameters=complexObj, paramType=param.in_)
                    
                    apiParams.append(cp)
                        
                elif type ==  "array":
                    items = schema.items
                    
                    ai: ArrayItem = self.get_items_in_array_datatype(items, name)
                    
                    cp = ParamProp(propertyName=name, type=type, arrayProp=ai, paramType=param.in_)
                    
                    apiParams.append(cp)
                        
                else:
                    apiParams.append(ParamProp(name, type, paramType=param.in_))
                                     
        return apiParams
        
    
    def create_mutator_api(self, apiObj, path):
        
        if not apiObj.post is None:
            
            api = Api()
            api.path = path
            api.verb = ApiVerb.POST
            
            api.parameters = self.obtain_parameters(apiObj.post)
            api.body = self.get_mutatorapi_body_props(apiObj.post)         
            
            return True, api
        
        return False, None
           
             
        
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
                
                cp = ParamProp(propertyName=propName, type="object", parameters=complexObj)
                
                continue
                
            else:
                #base case - primitive type
                if not type == "array":
                    
                    cp = ParamProp(propertyName=propName, type=type, format=format)
                    result.append(cp)
                    continue
                        
                if type == "array": #handles array of either complex object or primitives
                    
                    items =  schema.items # items exist for array type and is a class not iteratable
                    
                    arrayItem = self.get_items_in_array_datatype(items, propName)
                    
                    cp = ParamProp(propertyName=propName, type="array", parameters=None, arrayProp=arrayItem)
                    result.append(cp)   
    
    def get_complex_object_datatype(self, schema, result: list):
                
        # complex object type can be nested complex objects, array or primitive type
        # *roadmap: support getting parameters from example in addition to properties
          
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
                
                cp = ParamProp(propertyName=propName, type="object", parameters=nestedObj)
                
                result.append(cp)
                
            elif type == "array":
                
                arrayItem = self.get_items_in_array_datatype(schema.items, propName) #recursive method
                cp = ParamProp(propertyName=propName, type="array", arrayProp=arrayItem)
                result.append(cp)
            
            # is primitive type
            else:
                cp = ParamProp(propertyName=propName, type=type, format=format)
                result.append(cp)
                                    
    # ParamProp.parameters will be populated with new ParamProp of item in array
    def get_items_in_array_datatype(self, items, propertyName="") -> ArrayItem:
        
        # array can contain complex object or primitive type
        # does not currently support for nested array
        
        if items is None:
            ai = ArrayItem(type="string") # default to string not such use case of item=None may not be possible
            return ai
        
        isPrimitive, type = self.is_array_item_primitive_type(items)

        # handles array item is of primitive type
        if isPrimitive:
            ai = ArrayItem(type=type) 
            return ai
        
        if type == "object":
                        
            complexObject = []
                    
            self.get_complex_object_datatype(items, complexObject) # items is of Schema type
            
            ai = ArrayItem(type=type, parameters=complexObject) 
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
            
            result.append(ParamProp(propName, type, format=format))
            
            
    # requestBody and content are optional in OpenApi3 for Post/Put/Patch
    # check for existence to prevent error
    def get_mutatorapi_body_props(self, mutatorOperation) -> list:
        
        appJsonContentType = 'application/json'
        formDataWWWFormContentType = 'application/x-www-form-urlencoded'
        
        # Multipart requests combine one or more sets of data into a single body, separated by boundaries.
        # Typically use these requests for file uploads and for transferring data of several types in a single request
        # (for example, a file along with a JSON object)
        multipartFormContentType = 'multipart/form-data' # single file upload, multi-files upload, or Json data + file upload
        streamFileUploadContentType = 'application/octet-stream'
        appPdfContentType = 'application/pdf'
        imagePngContentType = 'image/png'
        imageAllContentType = 'image/*'
        sameForOthersContentType = "*/*" #https://swagger.io/docs/specification/media-types/
        
        contentResult = []
        properties = None
        
        if not mutatorOperation.requestBody is None:
            
            if hasattr(mutatorOperation.requestBody, 'properties'): # $ref: '#/components/name'. Class = Schema, Assume Json
                properties = mutatorOperation.requestBody.properties
                self.get_nested_content_properties(properties, contentResult)
                return contentResult
            
            if hasattr(mutatorOperation.requestBody, 'content'): # if content exists
                
                content = mutatorOperation.requestBody.content
                
                # */*
                if hasattr(content, sameForOthersContentType) or self.has_attribute(content, sameForOthersContentType): 
                    sameForOthers = content[sameForOthersContentType]
                    
                    schema = sameForOthers.schema
                                      
                    #handle array params
                    if schema.type == "array":
                        self.get_items_in_array_datatype(schema.items, "")
                    else:
                        properties = sameForOthers.schema.properties
                    
                        if not properties is None:
                            self.get_form_data_keyval(properties, contentResult) #same handling as for keyval
                            
                # application/json
                if hasattr(content, appJsonContentType) or self.has_attribute(content, appJsonContentType): 
                    jsonContent = content[appJsonContentType]
                    properties = jsonContent.schema.properties
                    
                    if not properties is None:
                        self.get_nested_content_properties(properties, contentResult)
                
                # application/x-www-form-urlencoded
                if hasattr(content, formDataWWWFormContentType) or self.has_attribute(content, formDataWWWFormContentType):
                    formContent = content[formDataWWWFormContentType] 
                    properties = formContent.schema.properties
                    
                    if not properties is None:
                        self.get_nested_content_properties(properties, contentResult)
                   
                # multipart/form-data
                if hasattr(content, multipartFormContentType) or self.has_attribute(content, multipartFormContentType):
                    multipartFormContent = content[multipartFormContentType]
                    properties = multipartFormContent.schema.properties
                    
                    if not properties is None:
                        self.get_nested_content_properties(properties, contentResult)
                
                # assume file upload base on media type with no property name
                if (hasattr(content, streamFileUploadContentType) or self.has_attribute(content, streamFileUploadContentType) or
                    hasattr(content, appPdfContentType) or self.has_attribute(content, appPdfContentType) or
                    hasattr(content, imagePngContentType) or self.has_attribute(content, imagePngContentType) or
                    hasattr(content, imageAllContentType) or self.has_attribute(content, imageAllContentType)):
                    
                    propName = "fileupload" # fixed name for file
                    contentResult.append(ParamProp(propName, 'string', 'binary'))
                
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
                
        
            
           
        