import unittest
from corpora_mutator import CorporaMutator

class TestCorporaMutator(unittest.TestCase):
    
    def test_mutate_single(self):
        
        g = CorporaMutator()
        
        g.mutate_single('a quick brown fox jumps over a grey hare')
        
        for x in range(0, 50):
            val = g.next_corpora()
            print(val)
            self.assertIsNotNone(val)
            self.assertTrue(isinstance(val, str))
            
        
        
if __name__ == '__main__':
    unittest.main()