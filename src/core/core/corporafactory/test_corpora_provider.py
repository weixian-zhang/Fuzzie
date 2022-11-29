

import unittest
from corpora_provider import CorporaProvider

class TestImageCorpora(unittest.TestCase):
    
    def test_image_corpora(self):
        
        g = CorporaProvider()
        g.load_all()
        
        boolVal = g.boolCorpora.next_corpora()
        self.assertTrue(boolVal != '')
        
        
if __name__ == '__main__':
    unittest.main()