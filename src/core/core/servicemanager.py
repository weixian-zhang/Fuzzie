# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext, ApiFuzzCaseSet
from webapi_fuzzer import WebApiFuzzer

from eventstore import EventStore
from db import  get_fuzzcontext, get_fuzzcontexts, insert_db_fuzzcontext
from sqlalchemy.sql import select, insert

import asyncio
import json
from datetime import datetime

class ServiceManager:
    
    def __init__(self) -> None:   
           
        self.eventstore = EventStore()
    
        
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
                            requestMessageSingle = '',
                            requestMessageFilePath = '',
                            openapi3FilePath = openapi3FilePath,
                            fuzzMode= fuzzMode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            authnType=authnType)
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        insert_db_fuzzcontext(fuzzcontext)
        
        return fuzzcontext
    
    def get_fuzzcontexts(self) -> list[ApiFuzzContext]:
        return get_fuzzcontexts()
    

    
    # def get_fuzzcontext(self, Id) -> ApiFuzzContext:
    #     return get_fuzzcontext(Id)
    
    async def fuzz(self, 
                   Id, basicUsername = '', basicPassword= '', 
                   bearerTokenHeader= '', bearerToken= '', 
                   apikeyHeader= '', apikey= '') -> None:
        
        fuzzcontext = self.get_fuzzcontext(Id)
        
        webapifuzzer = WebApiFuzzer(fuzzcontext, 
                                    basicUsername = basicUsername, 
                                    basicPassword= basicPassword, 
                                    bearerTokenHeader= bearerTokenHeader,
                                    bearerToken= bearerToken, 
                                    apikeyHeader=  apikeyHeader, 
                                    apikey= apikey)
        
        await webapifuzzer.fuzz()
        
        print('a')
        
    
    
    
    
        

    