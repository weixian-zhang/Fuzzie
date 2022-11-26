import unittest
from datetime_corpora import DateTimeCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def test_generate_password_corpora(self):
        
        g = DateTimeCorpora()
        g.load_corpora()
        
        for x in range(0, 50):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
        
        
if __name__ == '__main__':
    unittest.main()