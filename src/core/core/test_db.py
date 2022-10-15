import unittest
from db import apifuzzcontext_TableName, api_fuzzcontex_table, dbconn
from sqlalchemy.sql import select

class TestFuzzManager(unittest.TestCase):
    
        
    def test_query_apifuzzcontext(self):
        query = select([api_fuzzcontex_table])
        results = dbconn.execute(query)
        results.fetchall()
    

if __name__ == '__main__':
    unittest.main()