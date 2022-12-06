

import unittest
from boolean_corpora import BoolCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def test_boolean_corpora(self):
        
        g = BoolCorpora()
        
        for x in range(0, 500):
            val = g.next_corpora()
            #self.assertIsNotNone(val)
        
        
if __name__ == '__main__':
    unittest.main()