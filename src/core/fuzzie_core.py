
import sys

sys.path.insert(0, './api-initmanager')
from openapi3_init_manager import OpenApi3ApiInitManager

class TestCase:
    data = {}
    request = {}
    response = {}
    

class Fuzzie:
    
    def __init__(self, openapiUrl = "", openapiFilePath="", requestTextFilePath="", requestTextSingleString="") -> None:
        self.openapiUrl: str = ""
        self.openapiFilePath: str = ""
        self.requestTextFilePath: str = ""
        self.requestTextSingleString: str = ""
    
    
    def fuzz(self):
        
        print(f'discover API schema with OpenApi3 Url: {self.openapiUrl}')
    
#TODO

# API schema source from client
    # openapi3 url
    # openapi3 file path
    # .fuzzie file path - that describes api schema 
    # textual api string
    
    # create ApiContext from api source
    
    # fuzzing - 