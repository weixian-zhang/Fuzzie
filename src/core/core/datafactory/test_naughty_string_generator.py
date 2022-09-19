import unittest
from naughty_string_generator import NaughtyStringGenerator

class TestNaughtStringGenerator(unittest.TestCase):
    
    def test_get_naughty_string(self):
        
        g = NaughtyStringGenerator()
        
        for x in range(0, 500):
            ns = g.NextData()
            self.assertIsNotNone(ns)
            self.assertTrue(isinstance(ns, str))
        
        
if __name__ == '__main__':
    unittest.main()