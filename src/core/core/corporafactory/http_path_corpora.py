import os, sys
import asyncio
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from sqlalchemy.orm import scoped_session
from db import session_factory, DiscoveryWebPathTable
from eventstore import EventStore
import os

class HttpPathCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HttpPathCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        self.data = {}
        
        self.es = EventStore()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1        

    
    def load_corpora(self):
        if len(self.data) > 0:
            return
        
        Session = scoped_session(session_factory)
        
        # first 350,000 passwords
        rows = Session.query(DiscoveryWebPathTable.c.RowNumber, DiscoveryWebPathTable.c.Content).all()
        
        self.data = rows
        
        Session.close()        
        
    def next_corpora(self):
            
        if self.rowPointer > (len(self.data) - 1):
            self.rowPointer = 1
        
        data = self.data[self.rowPointer][1]   # [1] is 'content'
        
        self.rowPointer += 1
        
        return data
        