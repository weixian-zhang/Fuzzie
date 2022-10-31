import unittest

import os, sys
from pathlib import Path
datafacPath = os.path.join(os.path.dirname(Path(__file__)), 'datafactory')
dbPath = os.path.join(os.path.dirname(Path(__file__)), 'datafactory/data')
modelsPath = os.path.join(os.path.dirname(Path(__file__)), 'models')
sys.path.insert(0, datafacPath)
sys.path.insert(0, dbPath)
sys.path.insert(0, modelsPath)

from db import (ApiFuzzContextTable, ApiFuzzCaseSetTable,  metadata, session_factory, 
                get_naughtystring_by_id, get_naughtyusername_by_id, get_naughtypassword_by_id,
                get_fuzzContextSetRuns)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import select, insert
import json

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.webapi_fuzzcontext import FuzzMode, ApiFuzzContext
from eventstore import EventStore

from datetime import datetime
import os
from pathlib import Path
openapi3TestDataYamlPath = os.path.join(os.path.dirname(Path(__file__)), 'api_discovery\\testdata')

class TestFuzzManager(unittest.TestCase):
    
    def setUp(self):
        self.metadata = metadata

    def test_get_fuzzContextSetRuns(self):
        
        r = get_fuzzContextSetRuns()
        self.assertTrue(len(r) > 0)
        
        
    def test_get_naughtystring(self):
        
        s = get_naughtystring_by_id(1)
        self.assertTrue(s != '')
        
    def test_get_naughtyusername(self):
        
        s = get_naughtyusername_by_id(1)
        self.assertTrue(s != '')
        
    def test_get_naughtypassword(self):
        
        s = get_naughtypassword_by_id(1)
        self.assertTrue(s != '')
        
    def test_query_apifuzzcontext_join_fuzzCaseSet(self):
        query = select([ApiFuzzContextTable])
        Session = scoped_session(session_factory)
        results = Session.execute(query)
        results.fetchall()
        
        Session.close()
        
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
                            authnType='Anonymous')
        
        fuzzcontext: ApiFuzzContext = fcc.create_fuzzcontext(apicontext)

        fuzzcontextStmt = (
            insert(ApiFuzzContextTable).
            values(
                   Id=fuzzcontext.Id, 
                   datetime=datetime.now(),
                   name = fuzzcontext.name,
                    hostname = fuzzcontext.hostname,
                    port = fuzzcontext.port,
                    fuzzMode = fuzzcontext.fuzzMode,
                    fuzzcaseToExec = fuzzcontext.fuzzcaseToExec,
                    authnType = 'Anonymous')
         )
        
        Session = scoped_session(session_factory)
        
        Session.execute(fuzzcontextStmt)
        
        if len(fuzzcontext.fuzzcaseSets) > 0:
            for fcset in fuzzcontext.fuzzcaseSets:
                header = json.dumps(fcset.headerDataTemplate)
                body = json.dumps(fcset.bodyDataTemplate)
                
                fcSetStmt = (
                    insert(ApiFuzzCaseSetTable).
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
                
                Session.execute(fcSetStmt)
        
        Session.close()
    

if __name__ == '__main__':
    unittest.main()