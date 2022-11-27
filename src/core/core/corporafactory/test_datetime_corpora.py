import unittest
from datetime_corpora import DateTimeCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def setUp(self):
         self.dtCorpora = DateTimeCorpora()
         self.dtCorpora.load_corpora()
   
    
    def test_generate_time_corpora(self):

        for x in range(0, 50):
            val = self.dtCorpora.next_time_corpora()
            self.assertIsNotNone(val)
            
    def test_generate_date_corpora(self):
    
        for x in range(0, 50):
            val = self.dtCorpora.next_date_corpora()
            self.assertIsNotNone(val)
            
    def test_generate_datetime_corpora(self):
        
        for x in range(0, 50):
            val = self.dtCorpora.next_datetime_corpora()
            self.assertIsNotNone(val)
        
        
if __name__ == '__main__':
    unittest.main()