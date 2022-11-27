import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from sqlalchemy.orm import scoped_session
from db import session_factory, SeclistXSSTable, SeclistSqlInjectionTable, SeclistBLNSTable
import asyncio
import random
from multiprocessing import Lock
from eventstore import EventStore

class StringCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StringCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        self.es = EventStore()
        self.lock = Lock()
        self.rowPointer = 1
        self.xssRowPointer = 1
        self.sqliRowPointer = 1
        self.blnsRowPointer = 1
        self.xss = {}
        self.sqli = {}
        self.blns = {}
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1
    
    def load_corpora(self):
        
        if len(self.xss) > 0 and len(self.sqli) and len(self.blns):
            return
        
        try:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.create_task(self.load_blns()),
                loop.create_task(self.load_sqli()),
                loop.create_task(self.load_xss()),
            ]
            
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception as e:
            self.es.emitErr(e)
        
        
    async def load_xss(self):
        
        self.lock.acquire()
        
        Session = scoped_session(session_factory)
        
        rows = Session.query(SeclistXSSTable.c.RowNumber, SeclistXSSTable.c.Content).all()
        
        Session.close()
        
        for row in rows:
            
            rowDict = row._asdict()
            rn = rowDict['RowNumber']
            content = rowDict['Content']
            
            self.xss[rn] = content
        
        self.lock.release()
    
    async def load_sqli(self):
        
        self.lock.acquire()
        
        Session = scoped_session(session_factory)
        
        rows = Session.query(SeclistSqlInjectionTable.c.RowNumber, SeclistSqlInjectionTable.c.Content).all()
        
        Session.close()
        
        for row in rows:
            
            rowDict = row._asdict()
            rn = rowDict['RowNumber']
            content = rowDict['Content']
            
            self.sqli[rn] = content
        
        self.lock.release()
        
    async def load_blns(self):
        
        self.lock.acquire()
        
        Session = scoped_session(session_factory)
        
        rows = Session.query(SeclistBLNSTable.c.RowNumber, SeclistBLNSTable.c.Content).all()
        
        Session.close()
        
        for row in rows:
            
            rowDict = row._asdict()
            rn = rowDict['RowNumber']
            content = rowDict['Content']
            
            self.blns[rn] = content
        
        self.lock.release()
        

    def next_corpora(self):
        
        datasource = self.blns
        
        randInt = random.randint(0, 2)
        
        match randInt:
            case 0:
                datasource = self.blns
            case 1:
                datasource = self.xss
            case 2:
                datasource = self.sqli
            
        if self.rowPointer > (len(datasource) - 1):
            self.rowPointer = 1
            
        data = datasource[self.rowPointer]
        
        self.rowPointer += 1
        
        return data
    
    def next_xss_corpora(self):
        
        if self.xssRowPointer > (len(self.xss) - 1):
            self.xssRowPointer = 1
            
        data = self.xss[self.xssRowPointer]
        
        self.xssRowPointer += 1
        
        return data
    
    def next_sqli_corpora(self):
        
        if self.sqliRowPointer > (len(self.sqli) - 1):
            self.sqliRowPointer = 1
            
        data = self.sqli[self.sqliRowPointer]
        
        self.sqliRowPointer += 1
        
        return data
    
    def next_blns_corpora(self):
        
        if self.blnsRowPointer > (len(self.blns) - 1):
            self.blnsRowPointer = 0
            
        data = self.blns[self.blnsRowPointer]
        
        self.blnsRowPointer += 1
        
        return data
    
    
    def reset_cursor(self):
        self.rowPointer = 1
        self.xssRowPointer = 1
        self.sqliRowPointer = 1
        self.blnsRowPointer = 1