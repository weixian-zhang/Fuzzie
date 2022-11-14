# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext
from graphql_models import ApiFuzzContext_Runs_ViewModel
from webapi_fuzzer import WebApiFuzzer
from automapper import mapper
from eventstore import EventStore, MsgType
from db import  (get_fuzzcontext, 
                 get_caseSets_with_runSummary, 
                 insert_db_fuzzcontext, 
                 get_fuzzContexts_and_runs)
from sqlalchemy.sql import select, insert
import base64

import threading, time
from datetime import datetime
import queue

def bgWorkerDataToClient():
    
    while True:
        
        try:
            data = ServiceManager.dataQueue.get()
        
            if data != '':
                ServiceManager.eventstore.send_websocket(data, MsgType.FuzzEvent)
                
            time.sleep(1)
        except Exception as e:
            print(e)
        
        

class ServiceManager:
    
    eventstore = EventStore()
    dataQueue = queue.Queue()
    bgWorkerDataToClient = None
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServiceManager, cls).__new__(cls)
            threading.Thread(target=bgWorkerDataToClient, daemon=True).start()
        return cls.instance
    
    def __init__(self) -> None:   
        pass
    
    def new_api_fuzzcontext(self, apiDiscoveryMethod,  
                                isanonymous,
                                name,
                                requestTextContent,
                                requestTextFilePath,
                                openapi3FilePath,
                                openapi3Url,
                                openapi3Content,
                                basicUsername,
                                basicPassword,
                                bearerTokenHeader,
                                bearerToken,
                                apikeyHeader,
                                apikey,
                                hostname,
                                port,
                                fuzzcaseToExec,
                                authnType):
        
        openapi3Dis = OpenApi3ApiDiscover()
        isApiDisOK = True
        error = ''
        apicontext= None
        
        # rtStr=  base64.b64decode(requestTextContent).decode('UTF-8')
        openapi3Str=  base64.b64decode(openapi3Content).decode('UTF-8')
        
        if apiDiscoveryMethod == 'openapi3':
            isApiDisOK, error, apicontext = openapi3Dis.create_apicontext_from_openapi3(openapi3Str)
        elif apiDiscoveryMethod == 'request-text':
            pass
        
        if not isApiDisOK:
            return False, error
            
        fcc = OpenApi3FuzzContextCreator()
        
        fuzzcontext = fcc.new_fuzzcontext(  apiDiscoveryMethod=apiDiscoveryMethod,
                                            apicontext=apicontext,
                                            name=name,
                                            hostname=hostname,
                                            port=port,
                                            requestTextContent = requestTextContent,
                                            requestTextFilePath = requestTextFilePath,
                                            openapi3FilePath = openapi3FilePath,
                                            openapi3Url = openapi3Url,
                                            openapi3Content = openapi3Content,
                                            fuzzcaseToExec=fuzzcaseToExec,
                                            authnType=authnType,
                                            isanonymous=isanonymous,
                                            basicUsername=basicUsername,
                                            basicPassword=basicPassword,
                                            bearerTokenHeader=bearerTokenHeader,
                                            bearerToken=bearerToken,
                                            apikeyHeader=apikeyHeader,
                                            apikey=apikey)
        
        insert_db_fuzzcontext(fuzzcontext)
        
        # savedFC = get_fuzzcontext(fuzzcontext.Id)
        
        # fcView = mapper.to(ApiFuzzContext_Runs_ViewModel).map(savedFC)
        
        return True, ''
        
        
        

    # def discover_openapi3_by_filepath_or_url(self,
    #                         hostname,
    #                         authnType,
    #                         port=443,
    #                         name='',
    #                         openapi3FilePath = '',
    #                         openapi3Url = '',
    #                         fuzzMode= 'Quick',
    #                         numberOfFuzzcaseToExec=100):
        
    #     openapi3Dis = OpenApi3ApiDiscover()
    #     apicontext= None
        
    #     if openapi3FilePath != '':
    #         apicontext = openapi3Dis.load_openapi3_file(openapi3FilePath)
    #     else:
    #         apicontext = openapi3Dis.load_openapi3_url(openapi3Url)
        
    #     fcc = OpenApi3FuzzContextCreator()
    #     fcc.new_fuzzcontext(
    #                         name=name,
    #                         hostname=hostname,
    #                         port=port,
    #                         requestMessageText = '',
    #                         requestMessageFilePath = '',
    #                         openapi3FilePath = openapi3FilePath,
    #                         fuzzMode= fuzzMode,
    #                         numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
    #                         authnType=authnType)
        
    #     fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
    #     insert_db_fuzzcontext(fuzzcontext)
        
    #     savedFC = get_fuzzcontext(fuzzcontext.Id)
        
    #     fcView = mapper.to(ApiFuzzContext_Runs_ViewModel).map(fuzzcontext)
        
    #     # fcView = ApiFuzzContext_Runs_ViewModel()
    #     # fcView.Id = savedFC.Id
    #     # fcView.datetime = savedFC.datetime
    #     # fcView.apiDiscoveryMethod = savedFC.apiDiscoveryMethod
    #     # fcView.apicontext = savedFC.apicontext
    #     # fcView.name = savedFC.name
    #     # fcView.hostname = savedFC.hostname
    #     # fcView.port = savedFC.port
    #     # fcView.requestTextContent  = savedFC.requestTextContent
    #     # fcView.requestTextFilePath  = savedFC.requestTextFilePath
    #     # fcView.openapi3FilePath  = savedFC.openapi3FilePath
    #     # fcView.openapi3Url  = savedFC.openapi3Url
    #     # fcView.openapi3Content  = savedFC.openapi3Content
    #     # fcView.fuzzcaseToExecsavedFC.fuzzcaseToExec
    #     # fcView.authnTypesavedFC.authnType
    #     # fcView.isanonymous = savedFC.isanonymous
    #     # fcView.basicUsername = savedFC.basicUsername
    #     # fcView.basicPassword = savedFC.basicPassword
    #     # fcView.bearerTokenHeader = savedFC.bearerTokenHeader
    #     # fcView.bearerToken = savedFC.bearerToken
    #     # fcView.apikeyHeader = savedFC.apikeyHeader
    #     # fcView.apikey = savedFC.apikey
        
    #     return fcView
    
    def get_caseSets_with_runSummary(self, fuzzcontextId):
        return get_caseSets_with_runSummary(fuzzcontextId)
    
    
    def get_fuzzContexts_and_runs(self) -> list[ApiFuzzContext_Runs_ViewModel]:
        return get_fuzzContexts_and_runs() 
    
    
    def get_fuzzcontext(self, Id) -> ApiFuzzContext:
        return get_fuzzcontext(Id)
    
    def fuzz(self, 
                   Id, basicUsername = '', basicPassword= '', 
                   bearerTokenHeader= '', bearerToken= '', 
                   apikeyHeader= '', apikey= '') -> None:
        
        fuzzcontext = self.get_fuzzcontext(Id)
        
        webapifuzzer = WebApiFuzzer(ServiceManager.dataQueue,
                                    fuzzcontext, 
                                    basicUsername = basicUsername, 
                                    basicPassword= basicPassword, 
                                    bearerTokenHeader= bearerTokenHeader,
                                    bearerToken= bearerToken, 
                                    apikeyHeader=  apikeyHeader, 
                                    apikey= apikey)
        
        webapifuzzer.fuzz()
        
    
    
    
    
        

    