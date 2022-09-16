import unittest
from hacked_username_generator import HackedUsernameGenerator

class TestHackedUsernameGenerator(unittest.TestCase):
    
    def test_get_naughty_string(self):
        
        g = HackedUsernameGenerator()
        
        for x in range(0, 50):
            val = g.NextData()
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
            
            print(val)
        
        
if __name__ == '__main__':
    unittest.main()