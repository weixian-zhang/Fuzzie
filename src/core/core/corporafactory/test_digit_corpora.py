import unittest
from digit_corpora import DigitCorpora

class TestDigitCorpora(unittest.TestCase):
    
    def test_generate_next_corpora(self):
        
        g = DigitCorpora()
        
        for x in range(0, 50):
            val = g.next_corpora()
            print(val)
            self.assertIsNotNone(val)
            
    def test_generate_float_corpora(self):
        
        g = DigitCorpora()
        
        for x in range(0, 50):
            val = g.float_corpora_strategy()
            print(val)
            self.assertIsNotNone(val)
            
    def test_generate_int_corpora(self):
        
        g = DigitCorpora()
        
        for x in range(0, 50):
            val = g.int_corpora_strategy()
            print(val)
            self.assertIsNotNone(val)
            
    def test_user_supplied_range(self):
        
        g = DigitCorpora()
        
        val1 = g.get_user_supplied_range(4.999, 6000.782728)
        self.assertIsNotNone(val1)
        
        val2 = g.get_user_supplied_range(4.999, '6000.782728')
        self.assertIsNotNone(val1)
        
        val3 = g.get_user_supplied_range(-312132131, 6000.782728)
        self.assertIsNotNone(val3)
        
        
        
if __name__ == '__main__':
    unittest.main()