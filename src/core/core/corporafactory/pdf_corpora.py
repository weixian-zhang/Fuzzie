
from fpdf import FPDF, HTMLMixin
import random
from datetime import datetime
import os, sys
from pathlib import Path
from faker import Faker

import os, sys
import asyncio
from pathlib import Path

currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from eventstore import EventStore

class CustomFPDF(FPDF, HTMLMixin):
    pass

class PDFCorpora():
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PDFCorpora, cls).__new__(cls)
        return cls.instance
    
    
    def __init__(self) -> None:
        
        self.es = EventStore()
        
        self.data = []
        
        self.faker = Faker()
        
    def load_corpora(self, size=500):
        if len(self.data) > 0:
            return
        
        for i in range(size):
            
            pdf = self.create_pdf()
            self.data.append(pdf)
        
        
    def next_corpora(self) -> bytearray:
        
        if len(self.data) == 0:
            return None
        
        randIdx = random.randint(0, len(self.data) - 1)
        
        return self.data[randIdx]
    
    # fpdf output doc
    # http://www.fpdf.org/en/doc/output.htm
    def create_pdf(self):
        
        
        html = f'''
            <html>
                <body>
                    <H1 align="center">Fuzzie PDF</H1>
                    <p>{datetime.now()}</p>
                    <table border="0" align="center" width="50%">
                    <thead>
                        <tr>
                            <th width="50%">
                            Name
                            </th>
                            <th width="50%">
                            Address
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>name</td>
                            <td>{self.faker.name()}</td>
                        </tr>
                        <tr>
                            <td>address</td>
                            <td>{self.faker.address()}</td>
                        </tr>
                    </tbody>
                    </table>
                </body>
            </html>
            '''
       
        pdf = CustomFPDF()
        pdf.add_page()
        pdf.author = 'Fuzzie'
        
        pdf.write_html(html)
        
        byteStr = pdf.output(dest='S').decode('latin-1')
       
        return byteStr
    
    def currDir(self):
        
        
        cDir = os.path.dirname(Path(__file__))
        return cDir
        
        
        
    