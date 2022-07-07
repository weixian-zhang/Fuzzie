from openapi3 import OpenAPI
import yaml   
import enum
import json

class ApiVerb(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5

#class ReqBodyComplexJsonValue:
    
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
    isFileUpload: bool = False
    

class ApiInitManager:
    
    def load_openapi3_yaml_file(self, file_path: str):
        
        try:
            
            with open(file_path) as f:
                specYaml = yaml.safe_load(f)
                
            apiContext = self.create_apicontext_from_openapi3_structure(specYaml)
                             
        except Exception as e:
            print(e)
            
            
    def create_apicontext_from_openapi3_structure(self, openapiYaml) -> ApiContext:
        
        try:
            
            apispec = OpenAPI(openapiYaml)
            
            
            
            apicontext = ApiContext()
            
            apicontext.title = apispec.info.title
            apicontext.version = apispec.info.version
            
            if not apispec.servers is None:
                for server in apispec.servers:
                    apicontext.baseUrl.append(server.url)
                    
                    
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
            api.hasGet = True
            
            return True, api
        
        return False, None
    
    def create_post_api(self, apiObj, path):
        
        #https://swagger.io/docs/specification/describing-request-body/
        #understand request-body structure, example/examples are part of spec
        #https://github.com/Dorthu/openapi3/blob/master/tests/ref_test.py
        
        #file upload
        #https://swagger.io/docs/specification/describing-request-body/file-upload/
        
        if not apiObj.post is None:
            
            api = Api()
            api.path = path
            api.verb = ApiVerb.POST
            api.hasPost = True
            
            contentBody = apiObj.post.requestBody.content
            
            if len(contentBody) > 0:
                    
                content = self.get_request_body_content(contentBody)
                
                if not jsonContent.schema is None:
                    properties = jsonContent.schema.properties
                    
                    for n in properties:
                        print(n)
                        type = properties[n].type
                        print(type)
                
            
            return True, api
        
        return False, None
    
    
    def get_request_body_content(self, postPutPatchContent):
        
        appJsonContentType = 'application/json'
        formDataWWWFormContentType = 'application/x-www-form-urlencoded'
        multipartFormContentType = 'multipart/form-data' # single file or form + file or multiple files without form data
        
        
        if self.has_attribute(postPutPatchContent, appJsonContentType):
            jsonContent = postPutPatchContent[appJsonContentType]
            
            props = jsonContent.schema.properties
            
            jDictResult = {}
            
            self.get_complex_json_properties(props, jDictResult)
                
        
        if self.has_attribute(postPutPatchContent, formDataWWWFormContentType):
            formDataWWWFormContent = postPutPatchContent[formDataWWWFormContentType] 
        
        
        if self.has_attribute(postPutPatchContent, multipartFormContentType):
            pass
        
        
    def get_complex_json_properties(self, jsonProperty, jDict):
        
        
        for propName in jsonProperty:
            
            propSchema = jsonProperty[propName]
            
            type = propSchema.type
            
            #recurse case - if has more properties means nested json
            if type == 'object':
                
                newJDict = {}
                
                jDict[propName] = newJDict
                
                return self.get_complex_json_properties(propSchema.properties, newJDict)
            
            
            #base case
            
            jDict[propName]= type
            
            
            
            # if not propSchema.properties is None:
            #     return self.get_complex_json_properties(newJDict, propSchema.properties)
            
            
            
            
            #key = f'{propName}:{type}'
            
                
            
            
            # if self.has_attribute(propSchema, 'properties'):
            #     moreJsonProp =  prop['properties']
            #     self.get_json_complex_structure(moreJsonProp)
                
        return jDict
    
    def has_attribute(self, obj, attrName):
        
        for k in obj:
            if k == attrName:
                return True
        
        return False
                
        
            
           
        