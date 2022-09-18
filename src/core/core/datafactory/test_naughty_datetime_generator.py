import unittest
from naughty_datetime_generator import  NaughtyDateTimeGenerator

class TestNaughtyDateTimeGenerator(unittest.TestCase):
    
    def test_get_all_datetime_formats(self):
        
        g = NaughtyDateTimeGenerator()
        
        df = g.NextData()
        
        
        
if __name__ == "__main__":
    unittest.main()