
import sys

sys.path.insert(0, './api-initmanager')
from openapi3_init_manager import OpenApi3ApiInitManager

class TestCase:
    data = {}
    request = {}
    response = {}
    

class Fuzzie:
    
    def __init__(self, openapiUrl = "", openapiFilePath="", fuzzieTextualApiFilePath="", textualApiString="") -> None:
        openapiUrl: str = ""
        openapiFilePath: str = ""
        fuzzieTextualApiFilePath: str = ""
        textualApiString: str = ""
    
    
    def fuzz(self):
        pass
    
#TODO

# API schema source from client
    # openapi3 url
    # openapi3 file path
    # .fuzzie file path - that describes api schema 
    # textual api string
    
    # create ApiContext from api source
    
    # fuzzing - 