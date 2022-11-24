import unittest
from password_corpora import PasswordCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def test_get_naughty_string(self):
        
        g = PasswordCorpora()
        
        for x in range(0, 50):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
        
        
if __name__ == '__main__':
    unittest.main()