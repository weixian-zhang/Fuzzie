import unittest
from naughty_digits_generator import NaughtyDigitGenerator

class TestNaughtStringGenerator(unittest.TestCase):
    
    def test_get_naughty_string(self):
        
        g = NaughtyDigitGenerator()
        
        for x in range(0, 50):
            ns = g.NextData()
            self.assertIsNotNone(ns)
            print(ns)
        
        
if __name__ == '__main__':
    unittest.main()