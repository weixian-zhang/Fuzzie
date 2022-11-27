import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from sqlalchemy.orm import scoped_session
from db import session_factory, SeclistCharTable

import os

class CharCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CharCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:

        self.data = {}
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1
        
        self.load_corpora()

    
    def load_corpora(self):
        
        if len(self.data) > 0:
            return
        
        Session = scoped_session(session_factory)
        
        rows = Session.query(SeclistCharTable.c.RowNumber, SeclistCharTable.c.Content).all()
        
        Session.close()
        
        for row in rows:
            
            rowDict = row._asdict()
            rn = rowDict['RowNumber']
            content = rowDict['Content']
            
            self.data[str(rn)] = content
            
        rows = None
        
    def next_corpora(self):
            
        if self.rowPointer > (len(self.data) - 1):
            self.rowPointer = 0
            
        data = self.data[str(self.rowPointer)]
        
        self.rowPointer += 1
        
        return data
        
        