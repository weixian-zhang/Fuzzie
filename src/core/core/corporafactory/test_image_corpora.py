

import unittest
from image_corpora import ImageCorpora

class TestImageCorpora(unittest.TestCase):
    
    def test_image_corpora(self):
        
        g = ImageCorpora()
        g.load_corpora()
        
        for x in range(0, 10):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            
            fileName = f'C:\\Users\weixzha\\desktop\image-{str(x)}.png'
            
            f = open(fileName, "wb")
            f.write(val)
            f.close()
        
        
if __name__ == '__main__':
    unittest.main()