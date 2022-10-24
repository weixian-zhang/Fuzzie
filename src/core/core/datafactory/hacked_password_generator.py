import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from sqlalchemy.orm import sessionmaker, scoped_session
from db import session_factory, get_naughtypassword_by_id

from datagen import DataGenerator
import os

class HackedPasswordGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1

        self.dbsize = self.get_dbsize()
        
        
    def NextData(self):
        
        if self.rowPointer > self.dbsize:
            self.rowPointer = 1
        
        result = get_naughtypassword_by_id(self.rowPointer)
        
        self.rowPointer += 1
        
        return result
        
        
    def get_dbsize(self):
        tsql = f'''
            SELECT count(1)
            FROM NaughtyPassword
        '''
        
        self.cursor.execute(tsql)
        
        count = self.cursor.fetchone()[0]
        
        return count