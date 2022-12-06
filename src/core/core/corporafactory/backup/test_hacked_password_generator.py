import unittest
from hacked_password_generator import HackedPasswordGenerator

class TestHackedPasswordGenerator(unittest.TestCase):
    
    def test_get_naughty_string(self):
        
        g = HackedPasswordGenerator()
        
        for x in range(0, 50):
            val = g.NextData()
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
        
        
if __name__ == '__main__':
    unittest.main()