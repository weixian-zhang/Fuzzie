import unittest
from naughty_datetime_generator import  NaughtyDateTimeGenerator

class TestNaughtyDateTimeGenerator(unittest.TestCase):
    
    def test_get_all_datetime_formats(self):
        
        g = NaughtyDateTimeGenerator()
        
        count = 0
        while count <= 100:   
            print(g.NextData())
            count += 1
        
        
        
if __name__ == "__main__":
    unittest.main()