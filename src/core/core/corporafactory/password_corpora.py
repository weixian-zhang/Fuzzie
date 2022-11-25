import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from sqlalchemy.orm import scoped_session
from db import session_factory, SeclistPasswordTable

from corpora_base import CorporaBase
import os

class PasswordCorpora(CorporaBase):
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PasswordCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        super().__init__()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1

    
    def load_corpora(self):
        
        if len(self.data) > 0:
            return
        
        Session = scoped_session(session_factory)
        
        rows = Session.query(SeclistPasswordTable.c.RowNumber, SeclistPasswordTable.c.Content).all()
        
        Session.close()
        
        for row in rows:
            
            rowDict = row._asdict()
            rn = rowDict['RowNumber']
            content = rowDict['Content']
            
            self.data[str(rn)] = content
            
        rows = None
        