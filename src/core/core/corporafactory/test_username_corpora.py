import unittest
from username_corpora import UsernameCorpora

class TestUsernameCorpora(unittest.TestCase):
    
    def test_generate_password_corpora(self):
        
        g = UsernameCorpora()
        g.load_corpora()
        
        for x in range(0, 500):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
        
        
if __name__ == '__main__':
    unittest.main()