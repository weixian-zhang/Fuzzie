# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext
from graphql_models import ApiFuzzContextViewModel
from webapi_fuzzer import WebApiFuzzer

from eventstore import EventStore, MsgType
from db import  get_fuzzcontext, get_fuzzcontexts, insert_db_fuzzcontext, get_fuzzContextSetRuns
from sqlalchemy.sql import select, insert

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



        
    def discover_openapi3_by_filepath_or_url(self,
                            hostname,
                            authnType,
                            port=443,
                            name='',
                            openapi3FilePath = '',
                            openapi3Url = '',
                            fuzzMode= 'Quick',
                            numberOfFuzzcaseToExec=100):
        
        openapi3Dis = OpenApi3ApiDiscover()
        apicontext= None
        
        if openapi3FilePath != '':
            apicontext = openapi3Dis.load_openapi3_file(openapi3FilePath)
        else:
            apicontext = openapi3Dis.load_openapi3_url(openapi3Url)
        
        fcc = OpenApi3FuzzContextCreator()
        fcc.new_fuzzcontext(
                            name=name,
                            hostname=hostname,
                            port=port,
                            requestMessageText = '',
                            requestMessageFilePath = '',
                            openapi3FilePath = openapi3FilePath,
                            fuzzMode= fuzzMode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            authnType=authnType)
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        insert_db_fuzzcontext(fuzzcontext)
        
        
        fcView = ApiFuzzContextViewModel()
        fcView.Id = fuzzcontext.Id
        fcView.datetime = fuzzcontext.datetime
        fcView.name = fuzzcontext.name
        
        return fcView
    
    # def get_fuzzcontexts(self) -> list[ApiFuzzContext]:
    #     return get_fuzzcontexts()
    
    
    def get_fuzzContexts(self) -> list[ApiFuzzContextViewModel]:
        return get_fuzzContextSetRuns() 
    
    
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
        
    
    
    
    
        

    