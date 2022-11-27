
from fpdf import FPDF
from string_corpora import StringCorpora
import random
import os

class PDFCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PDFCorpora, cls).__new__(cls)
        return cls.instance
    
    
    def __init__(self) -> None:
        
        self.pdf = FPDF()
        
        self.strCorpora = StringCorpora()
        self.strCorpora.load_corpora()
        
    def next_corpora(self) -> bytearray:
 
        # Add a page
        self.pdf.add_page()
        
        # set style and size of font
        # that you want in the pdf
        self.pdf.set_font("Arial", size = 15)
        
        randLines = random.randint(1, 40)
        
        for i in range(1, randLines):
            
            data = self.strCorpora.next_xss_corpora()
            
            # create a cell
            self.pdf.cell(400, 20, txt = data,
                    ln = i, align = 'C')
        
        fileName = 'output_file.pdf'
        
        byteStr = self.pdf.output(fileName, 'S').encode('latin-1')
        
        return byteStr
    
    