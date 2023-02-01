

import unittest
from image_corpora import ImageCorpora
import io
from corpora_provider import CorporaProvider

class TestImageCorpora(unittest.TestCase):
    
    def setUp(self) -> None:
            
        self.cp = CorporaProvider()
        self.cp.load_all()
        
        return super().setUp()
    
    def test_image_corpora(self):
        
        # g = ImageCorpora()
        # g.load_corpora()
        
        for x in range(0, 10):
            
            val: io.BytesIO = self.cp.imageCorpora.next_corpora()
            
            self.assertIsNotNone(val)
            
            content = val.read()
            
            fileName = f'C:\\Users\weixzha\\desktop\image-{str(x)}.png'
            
            f = open(fileName, "wb")
            f.write(content)
            f.close()
        
        
if __name__ == '__main__':
    unittest.main()