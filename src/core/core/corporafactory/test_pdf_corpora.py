import unittest

import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from pdf_corpora import PDFCorpora
from corpora_provider import CorporaProvider

class TestPasswordCorpora(unittest.TestCase):
    
    def setUp(self) -> None:
        
        self.cp = CorporaProvider()
        self.cp.load_all()
        
        return super().setUp()
    
    def test_pdf_corpora(self):
        
        
        for x in range(0, 10):
            
            pdfStr = self.cp.pdfCorpora.next_corpora()
            
            self.assertIsNotNone(pdfStr)
            
            fileName = f'C:\\Users\weixzha\\desktop\pdf-{str(x)}.pdf'
            
            data = pdfStr
            if isinstance(pdfStr, str):
                data = bytes(pdfStr, encoding='latin-1')
            
            f = open(fileName, "wb")
            f.write(data)
            f.close()
        
        
if __name__ == '__main__':
    unittest.main()