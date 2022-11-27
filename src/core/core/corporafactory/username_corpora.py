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

from corpora_provider import CorporaBase
import os

class UsernameCorpora(CorporaBase):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1

    
    def load_corpora(self):
        
        if len(self.data) > 0:
            return
        
        Session = scoped_session(session_factory)
        
        rows = Session.query(SeclistUsernameTable.c.RowNumber, SeclistUsernameTable.c.Content).all()
        
        Session.close()
        
        for row in rows:
            
            rowDict = row._asdict()
            rn = rowDict['RowNumber']
            content = rowDict['Content']
            
            self.data[str(rn)].append(content)
            
        rows = None

        