import unittest
from password_corpora import PasswordCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def test_generate_password_corpora(self):
        
        g = PasswordCorpora()
        g.load_corpora()
        
        for x in range(0, 5000):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
        
        
if __name__ == '__main__':
    unittest.main()