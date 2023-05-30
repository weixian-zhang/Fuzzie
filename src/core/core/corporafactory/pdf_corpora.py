
from fpdf import FPDF, HTMLMixin
import random
from datetime import datetime
import os, sys
from pathlib import Path

import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

import base64
from sqlalchemy.orm import scoped_session
from db import session_factory, SeclistPDFTable

from seclist_payload_corpora import SeclistPayloadCorpora
from eventstore import EventStore

class CustomFPDF(FPDF, HTMLMixin):
    pass

class PDFCorpora():
    
    def __new__(cls, payloadCorpora: SeclistPayloadCorpora):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PDFCorpora, cls).__new__(cls)
        return cls.instance
    
    
    def __init__(self, payloadCorpora: SeclistPayloadCorpora) -> None:
        
        self.es = EventStore()
        
        self.pdfs = {}
        
        self.payloadCorpora = payloadCorpora
        
    def load_corpora(self):
        
        if len(self.pdfs) > 0:
            return
        
        Session = scoped_session(session_factory)
        
        rows = Session.query(SeclistPDFTable.c.RowNumber, SeclistPDFTable.c.Content).all()
        
        Session.close()
        
        for row in rows:
            
            rowDict = row._asdict()
            rn = rowDict['RowNumber']
            content = rowDict['Content']
            
            self.pdfs[rn] = content
        
        
    def next_corpora(self) -> bytearray:
        
        if len(self.pdfs) == 0:
            return None
        
        randInt = random.randint(1, 10)
        
        data = None
        
        if randInt <= 7:
            randDataIdx = random.randint(1, len(self.pdfs) - 1)
            encoded = self.pdfs[randDataIdx]
            data = base64.b64decode(encoded)
        else:
            data = self.payloadCorpora.next_corpora()
            
        
        return data
    
        
        
        
    