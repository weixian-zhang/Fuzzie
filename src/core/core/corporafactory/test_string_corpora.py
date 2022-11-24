import unittest
from string_corpora import StringCorpora

class TestStringCorpora(unittest.IsolatedAsyncioTestCase):
    
    async def test_get_naughty_string(self):
        
        g = StringCorpora()
        
        await g.load_corpora()
        
        for x in range(0, 50):
            val1 = g.next_corpora()
            self.assertIsNotNone(val1)
            self.assertTrue(isinstance(val1, str))
            
            val2 = g.next_xss_corpora()
            self.assertIsNotNone(val2)
            self.assertTrue(isinstance(val2, str))
            
            val3 = g.next_sqli_corpora()
            self.assertIsNotNone(val3)
            self.assertTrue(isinstance(val3, str))
            
            val4 = g.next_blns_corpora()
            self.assertIsNotNone(val4)
            self.assertTrue(isinstance(val4, str))
        
        
if __name__ == '__main__':
    unittest.main()