import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from sqlalchemy.orm import scoped_session
from db import session_factory, SeclistUsernameTable
import os
import asyncio

from eventstore import EventStore

class UsernameCorpora:
    
    def __init__(self) -> None:
        super().__init__()
        
        self.es = EventStore()
        self.data = {}
        self.rowPointer = 0; #important as sqlitre autoincrement id starts from 1

    def load_corpora(self):
        try:
            if len(self.data) > 0:
                return
        
            Session = scoped_session(session_factory)
            
            rows = Session.query(SeclistUsernameTable.c.RowNumber, SeclistUsernameTable.c.Content).all()
            
            self.data = rows
            
            Session.close()
        except Exception as e:
            self.es.emitErr(e)

    
    def next_corpora(self):
            
        if self.rowPointer > (len(self.data) - 1):
            self.rowPointer = 0
            
        data = self.data[self.rowPointer][1]
        
        self.rowPointer += 1
        
        return data

        