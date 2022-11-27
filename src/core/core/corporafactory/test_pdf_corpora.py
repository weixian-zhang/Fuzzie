import unittest
from pdf_corpora import PDFCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def test_generate_password_corpora(self):
        
        g = PDFCorpora()
        
        for x in range(0, 10):
            val = g.next_corpora()
            self.assertIsNotNone(val)
            
            fileName = f'C:\\Users\weixzha\\desktop\pdf-{str(x)}.pdf'
            
            f = open(fileName, "wb")
            f.write(val)
            f.close()
        
        
if __name__ == '__main__':
    unittest.main()