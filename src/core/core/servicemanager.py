# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.fuzzcontext import FuzzMode, ApiFuzzContext
from eventstore import EventStore

from db import FuzzContextTable, FuzzCaseSetTable, dbconn, session
from sqlalchemy.sql import select, insert


import json
from datetime import datetime

class ServiceManager:
    
    def __init__(self) -> None:   
           
        self.eventstore = EventStore()
    
        
    def discover_openapi3_by_filepath(self,
                            hostname,
                            port,
                            filePath,
                            name='',
                            fuzzMode= 'Quick',
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicUsername='',
                            basicPassword='',
                            bearerTokenHeader='',
                            bearerToken='',
                            apikeyHeader='',
                            apikey=''):
        
        openapi3Dis = OpenApi3ApiDiscover()
        apicontext = openapi3Dis.load_openapi3_file(filePath)
        
        fcc = OpenApi3FuzzContextCreator()
        fcc.new_fuzzcontext(hostname=hostname,
                            port=port,
                            fuzzMode= fuzzMode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            isAnonymous=isAnonymous,
                            basicUsername=basicUsername,
                            basicPassword=basicPassword,
                            bearerTokenHeader=bearerTokenHeader,
                            bearerToken=bearerToken,
                            apikeyHeader=apikeyHeader,
                            apikey=apikey,
                            filePath=filePath)
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        self.insert_db_fuzzcontext(fuzzcontext)
        
        return fuzzcontext
    
    def get_fuzzcontexts(self):
        
        j = FuzzContextTable.join(FuzzCaseSetTable,
                FuzzContextTable.c.Id == FuzzCaseSetTable.c.fuzzcontextId)
        stmt = select(FuzzContextTable, FuzzCaseSetTable).select_from(j)
        results = dbconn.execute(stmt)
        fuzzcontext = results.fetchall()
                
        for u in fuzzcontext:
           fcDict = u._asdict()
           
           for k in fcDict:
                print(f'{k}:{fcDict[k]}')
        
        return fuzzcontext
    
        # result = (
        #             session.query(FuzzContextTable, FuzzCaseSetTable)
        #                 .filter(
        #                     FuzzContextTable.columns.Id == FuzzCaseSetTable.columns.fuzzcontextId
        #                 )
        #                 .all()
        #           )
        # return result
                                
        
        # query = select([FuzzContextTable])
        # results = dbconn.execute(query)
        # fcs = results.fetchall()
        # return fcs
    
    
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
                cookies = json.dumps(fcset.cookieDataTemplate)
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
                        cookieDataTemplate = cookies,
                        bodyDataTemplate =  body,
                        fuzzcontextId = fuzzcontext.Id
                        )
                )
                
                dbconn.execute(fcSetStmt)    
        

    