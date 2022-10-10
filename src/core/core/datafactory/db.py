
import sqlite3
import os

# sqlite json extension
#https://www.youtube.com/watch?v=yxuroInnJNs

class DB:
    
    def __init__(self) -> None:
        
        self.dbpath = os.path.join(os.path.dirname(__file__), "data\\fuzzie.sqlite")

        self.sqliteconn = sqlite3.connect(self.dbpath, isolation_level=None)
        
        self.cursor = self.sqliteconn.cursor()
    
    def fetch_one(self, tsql: str):
        
        self.cursor.execute(tsql)
        
        result = self.cursor.fetchone()[0]
        
        return result
    
    def fetch_many(self, tsql: str):
        
        self.cursor.execute(tsql)
    
        result = self.cursor.fetchmany()
        
    def insert(self, tsql: str):
        self.cursor.execute(tsql)