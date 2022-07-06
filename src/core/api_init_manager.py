from openapi3 import OpenAPI
import yaml   
import enum
import json

class ApiVerb(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

class ApiContext:
    
    baseUrl = []
    title: str = ''
    version: str = ''
    apis = []

class Api:
    
    path: str = ''
    operationId: str = ''
    verb: ApiVerb = ApiVerb.GET
    hasGet: bool = False
    hasPost: bool = False
    hasPut: bool = False
    hasDelete: bool = False
    

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
        
        #https://swagger.io/docs/specification/describing-request-body/
        #https://github.com/Dorthu/openapi3/blob/master/tests/ref_test.py
        
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
        
        if not apiObj.post is None:
            
            api = Api()
            api.path = path
            api.verb = ApiVerb.POST
            api.hasPost = True
            
            content = apiObj.post.requestBody.content
            
            if len(content) > 0:
                    
                jsonContent = content['application/json']
                
                if not jsonContent.schema is None:
                    properties = jsonContent.schema.properties
                    
                    for n in properties:
                        print(n)
                        type = properties[n].type
                        print(type)
                    
                bodyDict = json.dumps(jsonBody)
            
            return True, api
        
        return False, None
        
        
            
           
        