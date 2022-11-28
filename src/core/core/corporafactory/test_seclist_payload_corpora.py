
import unittest
from seclist_payload_corpora import SeclistPayloadCorpora

class TestSeclistPayloadCorpora(unittest.TestCase):
    
    def test_seclist_payload_corpora(self):
        
        g = SeclistPayloadCorpora()
        g.load_corpora()
        
        for x in range(0, 50):
            file = g.next_corpora()
            fn = file['filename']
            c = file['content']
            
            self.assertIsNotNone(fn)
            self.assertIsNotNone(c)
            
            

        
        
if __name__ == '__main__':
    unittest.main()