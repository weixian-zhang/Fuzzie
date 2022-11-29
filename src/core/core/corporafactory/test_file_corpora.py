import unittest
from file_corpora import FileCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def test_file_corpora(self):
        
        g = FileCorpora()
        g.load_corpora()
        
        for x in range(0, 50):
            val = g.next_corpora()
            self.assertIsNotNone(val)
        
        
if __name__ == '__main__':
    unittest.main()