import unittest
from naughty_file_generator import NaughtyFileGenerator

class TestNaughtyFileGenerator(unittest.TestCase):
    
    def test_get_naughty_string(self):
        
        g = NaughtyFileGenerator()
        
        for x in range(0, 30):
            val = g.NextData()
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
        
        
if __name__ == '__main__':
    unittest.main()