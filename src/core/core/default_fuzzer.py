from api_recognition.openapi3_init_manager import OpenApi3ApiInitManager


class TestCase:
    data = {}
    request = {}
    response = {}
    

class DefaultFuzzer:
    
    def __init__(self, openapiUrl = "", openapiFilePath="", requestTextFilePath="", requestTextSingleString="") -> None:
        self.openapiUrl: str = ""
        self.openapiFilePath: str = ""
        self.requestTextFilePath: str = ""
        self.requestTextSingleString: str = ""
    
    
    def fuzz(self):
        
        print(f'In DefaultFuzzer, discover API schema with OpenApi3 Url: {self.openapiUrl}')
    
#TODO

# API schema source from client
    # openapi3 url
    # openapi3 file path
    # .fuzzie file path - that describes api schema 
    # textual api string
    
    # create ApiContext from api source
    
    # fuzzing - 