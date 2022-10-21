# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext, ApiFuzzCaseSet
from webapi_fuzzer import WebApiFuzzer

from eventstore import EventStore
from db import FuzzContextTable, FuzzCaseSetTable, dbconn, get_fuzzcontext, get_fuzzcontexts
from sqlalchemy.sql import select, insert


import json
from datetime import datetime

class ServiceManager:
    
    def __init__(self) -> None:   
           
        self.eventstore = EventStore()
    
        
    def discover_openapi3_by_filepath_or_url(self,
                            hostname,
                            port=443,
                            name='',
                            openapi3FilePath = '',
                            openapi3Url = '',
                            fuzzMode= 'Quick',
                            numberOfFuzzcaseToExec=100,
                            isAnonymous=True,
                            basicUsername='',
                            basicPassword='',
                            bearerTokenHeader='',
                            bearerToken='',
                            apikeyHeader='',
                            apikey=''):
        
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
                            openapi3Url = openapi3Url,
                            fuzzMode= fuzzMode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            isAnonymous=isAnonymous,
                            basicUsername=basicUsername,
                            basicPassword=basicPassword,
                            bearerTokenHeader=bearerTokenHeader,
                            bearerToken=bearerToken,
                            apikeyHeader=apikeyHeader,
                            apikey=apikey)
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        self.insert_db_fuzzcontext(fuzzcontext)
        
        return fuzzcontext
    
    def get_fuzzcontexts(self) -> list[ApiFuzzContext]:
        return get_fuzzcontexts()
    
    def get_fuzzcontext(self, Id) -> ApiFuzzContext:
        return get_fuzzcontext(Id)
    
    def fuzz(self, Id) -> None:
        
        fuzzcontext = self.get_fuzzcontext(Id)
        
        webapifuzzer = WebApiFuzzer(fuzzcontext)
        
        webapifuzzer.fuzz()
        
    
    
    
    def insert_db_fuzzcontext(self, fuzzcontext: ApiFuzzContext):
        
        securityScheme = fuzzcontext.get_security_scheme().name

        fuzzcontextStmt = (
            insert(FuzzContextTable).
            values(
                   Id=fuzzcontext.Id, 
                   datetime=datetime.now(),
                   name = fuzzcontext.name,
                    hostname = fuzzcontext.hostname,
                    port = fuzzcontext.port,
                    fuzzMode = fuzzcontext.fuzzMode,
                    fuzzcaseToExec = fuzzcontext.fuzzcaseToExec,
                    authnType = securityScheme,
                    isAnonymous = fuzzcontext.isAnonymous,
                    basicUsername = fuzzcontext.basicUsername,
                    basicPassword = fuzzcontext.basicPassword,
                    bearerTokenHeader = fuzzcontext.bearerTokenHeader,
                    bearerToken = fuzzcontext.bearerToken,
                    apikeyHeader = fuzzcontext.apikeyHeader,
                    apikey = fuzzcontext.apikey
                   )
         )
        
        dbconn.execute(fuzzcontextStmt)
        
        if len(fuzzcontext.fuzzcaseSets) > 0:
            for fcset in fuzzcontext.fuzzcaseSets:
                header = json.dumps(fcset.headerDataTemplate)
                body = json.dumps(fcset.bodyDataTemplate)
                
                fcSetStmt = (
                    insert(FuzzCaseSetTable).
                    values(
                        Id=fcset.Id, 
                        selected = fcset.selected,
                        verb = fcset.verb,
                        path = fcset.path,
                        querystringNonTemplate = fcset.querystringNonTemplate,
                        bodyNonTemplate = fcset.bodyNonTemplate,
                        pathDataTemplate = fcset.pathDataTemplate,
                        querystringDataTemplate = fcset.querystringDataTemplate,
                        headerDataTemplate = header,
                        bodyDataTemplate =  body,
                        fuzzcontextId = fuzzcontext.Id
                        )
                )
                
                dbconn.execute(fcSetStmt)
                
    # def create_fuzzcontext_from_dict(self, rowDict):
    #     fuzzcontext = ApiFuzzContext()
    #     fuzzcontext.Id = rowDict['Id']
    #     fuzzcontext.datetime = rowDict['datetime']
    #     fuzzcontext.name = rowDict['name']
        
    #     fuzzcontext.requestMessageSingle = rowDict['requestMessageSingle']
    #     fuzzcontext.requestMessageFilePath = rowDict['requestMessageFilePath']
    #     fuzzcontext.openapi3FilePath = rowDict['openapi3FilePath']
    #     fuzzcontext.openapi3Url = rowDict['openapi3Url']
        
    #     fuzzcontext.hostname= rowDict['hostname']
    #     fuzzcontext.port= rowDict['port']
    #     fuzzcontext.fuzzMode= rowDict['fuzzMode']
    #     fuzzcontext.fuzzcaseToExec = rowDict['fuzzcaseToExec']
    #     fuzzcontext.authnType = rowDict['authnType']
    #     fuzzcontext.isAnonymous = rowDict['isAnonymous']
    #     fuzzcontext.basicUsername= rowDict['basicUsername']
    #     fuzzcontext.basicPassword = rowDict['basicPassword']
    #     fuzzcontext.bearerTokenHeader= rowDict['bearerTokenHeader']
    #     fuzzcontext.bearerToken = rowDict['bearerToken']
    #     fuzzcontext.apikeyHeader = rowDict['apikeyHeader']
    #     fuzzcontext.apikey = rowDict['apikey']
        
    #     return fuzzcontext
    

    # def create_fuzzcaseset_from_dict(self, rowDict):
    #     fcs = ApiFuzzCaseSet()
    #     fcs.Id = rowDict['fuzzCaseSetId']
    #     fcs.path = rowDict['path']
    #     fcs.pathDataTemplate = rowDict['pathDataTemplate']
    #     fcs.querystringDataTemplate= rowDict['querystringDataTemplate']
    #     fcs.bodyDataTemplate= rowDict['bodyDataTemplate']
    #     fcs.headerDataTemplate = rowDict['headerDataTemplate']
    #     fcs.querystringNonTemplate = rowDict['querystringNonTemplate']
    #     fcs.bodyNonTemplate = rowDict['bodyNonTemplate']
    #     fcs.selected = rowDict['selected']
    #     fcs.verb = rowDict['verb']
    #     return fcs
        

    