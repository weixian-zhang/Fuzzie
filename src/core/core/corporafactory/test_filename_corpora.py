

import unittest
from filename_corpora import FileNameCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def test_boolean_corpora(self):
        
        g = FileNameCorpora()
        
        for x in range(0, 1000):
            val = g.next_corpora()
            
            self.assertIsNotNone(val)
        
        
if __name__ == '__main__':
    unittest.main()