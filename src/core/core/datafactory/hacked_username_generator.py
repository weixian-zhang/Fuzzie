

from datagen import DataGenerator
import os
import sqlite3

import os, sys
from pathlib import Path
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from sqlalchemy.orm import sessionmaker, scoped_session
from db import get_naughtyusername_by_id, get_naughtyusername_row_count

class HackedUsernameGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1
        
        self.dbsize = self.get_dbsize()
        
        
    def NextData(self):
        
        if self.rowPointer > self.dbsize:
            self.rowPointer = 1
        
        result = get_naughtyusername_by_id(self.rowPointer)
        
        self.rowPointer += 1
        
        return result
        
        
    def get_dbsize(self):
        
        count = get_naughtyusername_row_count()
        
        return count