import unittest

from db import FuzzContextTable, FuzzCaseSetTable, dbconn, metadata
from sqlalchemy.sql import select, insert
import json

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext
from eventstore import EventStore

import shortuuid
from datetime import datetime
import os
from pathlib import Path
openapi3TestDataYamlPath = os.path.join(os.path.dirname(Path(__file__)), 'api_discovery\\testdata')

class TestFuzzManager(unittest.TestCase):
    
    def setUp(self):
        self.metadata = metadata

    def teardown(self):
        self.metadata.drop_all()
        
        
    def test_query_apifuzzcontext_join_fuzzCaseSet(self):
        query = select([FuzzContextTable])
        results = dbconn.execute(query)
        results.fetchall()
        
    def test_insert_apifuzzcontext(self):
        
        openapi3Yaml = os.path.join(openapi3TestDataYamlPath, 'testdata-openapi3-get-params-path-object.yaml')
        
        openapi3Dis = OpenApi3ApiDiscover()
        apicontext = openapi3Dis.load_openapi3_file(openapi3Yaml)
        
        fcc = OpenApi3FuzzContextCreator()
        fcc.new_fuzzcontext(
                            hostname='http://localhost',
                            port=50001,
                            fuzzMode= FuzzMode.Quick,
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicUsername='',
                            basicPassword='',
                            bearerTokenHeader='',
                            bearerToken='',
                            apikeyHeader='',
                            apikey='')
        
        fuzzcontext: ApiFuzzContext = fcc.create_fuzzcontext(apicontext)
        
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
    

if __name__ == '__main__':
    unittest.main()