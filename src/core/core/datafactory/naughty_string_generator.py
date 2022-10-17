

from datagen import DataGenerator
import os
import sqlite3

class NaughtyStringGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1

        self.dbpath = os.path.join(os.path.dirname(__file__), "data\\fuzzie.sqlite")

        self.sqliteconn = sqlite3.connect(self.dbpath, isolation_level=None)
        
        self.cursor = self.sqliteconn.cursor()
        
        self.dbsize = self.get_dbsize()
        
        
    def NextData(self):
        
        if self.rowPointer > self.dbsize:
            self.rowPointer = 1
        
        tsql = f'''
            SELECT Content
            FROM NaughtyString
            WHERE id = {self.rowPointer}
        '''
        
        self.cursor.execute(tsql)
        
        result = self.cursor.fetchone()[0]
        
        self.rowPointer += 1
        
        return result
        
        
    def get_dbsize(self):
        tsql = f'''
            SELECT count(1)
            FROM NaughtyString
        '''
        
        self.cursor.execute(tsql)
        
        count = self.cursor.fetchone()[0]
        
        return count