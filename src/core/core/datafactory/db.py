import sqlalchemy as db

import os, sys
from pathlib import Path
parentDir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, os.path.join(parentDir, 'models'))
from models.fuzzcontext import ApiFuzzContext

dbEngine=db.create_engine('sqlite:////data/fuzzie.sqlite')

connection = dbEngine.connect()






# import sqlite3
# import os

# # sqlite json extension
# #https://www.youtube.com/watch?v=yxuroInnJNs

# class DB:
    
#     def __init__(self) -> None:
        
#         self.dbpath = os.path.join(os.path.dirname(__file__), "data\\fuzzie.sqlite")

#         self.sqliteconn = sqlite3.connect(self.dbpath, isolation_level=None)
        
#         self.cursor = self.sqliteconn.cursor()
    
#     def fetch_one(self, tsql: str):
        
#         self.cursor.execute(tsql)
        
#         result = self.cursor.fetchone()[0]
        
#         return result
    
#     def fetch_many(self, tsql: str):
        
#         self.cursor.execute(tsql)
    
#         result = self.cursor.fetchmany()
        
#     def execute(self, tsql: str):
#         self.cursor.execute(tsql)