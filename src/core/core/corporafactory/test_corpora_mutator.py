import unittest
from corpora_mutator import CorporaMutator

class TestCorporaMutator(unittest.TestCase):
    
    def test_mutate_single(self):
        
        g = CorporaMutator()
        
        mutated = g.mutate_single('a quick brown fox jumps over a grey hare')
        
        for x in range(0, 50):
            val = mutated[x]
            self.assertIsNotNone(val)
            print(val)
            
    
    def test_mutate_list(self):
        
        g = CorporaMutator()
        
        mutated = g.mutate_list(['a quick brown fox jumps', 'over a grey hare', 'just do it'])
    
        for x in range(0, 50):
            val = mutated[x]
            self.assertIsNotNone(val)
            print(val)
    
    def test_heap_permute(self):
        
        g = CorporaMutator()
        
        items = [1,2,3]
        
        result = g.permutation(items, 0, len(items))
        
        print(result)
            
        
        
if __name__ == '__main__':
    unittest.main()