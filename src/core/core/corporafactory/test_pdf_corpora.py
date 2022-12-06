import unittest
from pdf_corpora import PDFCorpora

class TestPasswordCorpora(unittest.TestCase):
    
    def test_pdf_corpora(self):
        
        g = PDFCorpora()
        g.load_corpora()
        
        for x in range(0, 10):
            pdfStr = g.next_corpora()
            self.assertIsNotNone(pdfStr)
            
            fileName = f'C:\\Users\weixzha\\desktop\pdf-{str(x)}.pdf'
            
            f = open(fileName, "wb")
            f.write(bytes(pdfStr, 'latin-1'))
            f.close()
        
        
if __name__ == '__main__':
    unittest.main()