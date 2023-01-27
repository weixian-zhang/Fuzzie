import unittest
from user_supplied_corpora import StringMutateCorpora

class TestStringMutateCorpora(unittest.TestCase):
    
    def test_single_user_supplied_corpora(self):
        
        g = StringMutateCorpora()
        
        g.load_single('this is a very powerful fuzzer')
       
        for x in range(0, 500):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            print(val)
            
    def test_list_ofuser_supplied_corpora(self):
        
        g = StringMutateCorpora()
        
        my = [
            'Disneyland: “The happiest place on Earth.',
            'Do what you can’t.',
            'Move the way you want',
            'Is it in you'
        ]
        
        g.load_list(my)
       
        for x in range(0, 500):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            print(val)
            
        
        
if __name__ == '__main__':
    unittest.main()