from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover

import validators
from fuzzcontext_model import ApiFuzzContext
from eventstore import EventStore

class FuzzManager:
    
    def __init__(self,
                 eventstore: EventStore,
                 openapiUrl = "", 
                 openapiFilePath="", 
                 requestTextFilePath="", 
                 requestTextSingle="",
                 workingDirectory = "") -> None:
        
        self.fuzzContext: None
        
        self.workingDirectory = workingDirectory
        
        self.eventstore = eventstore
    
    
    def fuzz(self, json):
        
        print(f'In DefaultFuzzer, discover API schema with OpenApi3 Url: {self.openapiUrl}')
        
        openapiUrl = json["openapiUrl"]
        openapiFilePath = json["openapiFilePath"]
        openapiFilePath = json["openapiFilePath"]
        requestTextFilePath = json["requestTextFilePath"]
        requestTextSingle = json["requestTextSingle"]
        workingDirectory = json["workingDirectory"]
        
        if not openapiUrl == "" and not validators.url(openapiUrl):
            print("Invalid OpenApi Url")
            return
        
        
        self.fuzzContext = FuzzContext(openapiUrl, openapiFilePath, requestTextFilePath, requestTextSingle, workingDirectory)
    
        #TODO

        # API schema source from client
            # openapi3 url
            # openapi3 file path
            # .fuzzie file path - that describes api schema 
            # textual api string
            
            # create ApiContext from api source
            
            # fuzzing - 
            
            
        # call data factory prepare data
        
        #fuzzing
        
        #update progress