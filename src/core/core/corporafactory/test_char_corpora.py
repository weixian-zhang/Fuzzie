import unittest
from char_corpora import CharCorpora

class TestCharCorpora(unittest.TestCase):
    
    def test_generate_char_corpora(self):
        
        g = CharCorpora()
        
        for x in range(0, 500):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
        
        
if __name__ == '__main__':
    unittest.main()