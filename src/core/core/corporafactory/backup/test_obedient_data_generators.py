import sys, os
parentPath = os.getcwd() + "\core\core\corporafactory"
sys.path.append(parentPath)

import unittest
from obedient_data_generators import (ObedientIntegerGenerator, 
                                      ObedientFloatGenerator, 
                                      ObedientCharGenerator, 
                                      ObedientStringGenerator)

class TestObedientDataGenerator(unittest.TestCase):
               
            
    def test_obedient_int_gen(self):
        
        g = ObedientIntegerGenerator()
        
        for x in range(1, (len(g.data) + 10)):
           val = g.NextData()
           self.assertIsNotNone(val)
           self.assertTrue(val >= -100000 and val <= 100000)
           
           
    def test_obedient_float_gen(self):
            
        g = ObedientFloatGenerator()
        
        for x in range(1, 30):
           val = g.NextData()
           self.assertIsNotNone(val)
           self.assertTrue(val >= -100000.1 and val <= 100000.9)
           
    def test_obedient_char_gen(self):
            
        g = ObedientCharGenerator()
        
        for x in range(1, 30):
           val = g.NextData()
           self.assertIsNotNone(val)
           self.assertTrue(len(val) == 1)
           
    def test_obedient_string_gen(self):
            
        g = ObedientStringGenerator()
        
        for x in range(1, 30):
           val = g.NextData()
           self.assertIsNotNone(val)
           self.assertTrue(isinstance(val,str))
            
        
        
if __name__ == "__main__":
    unittest.main()