import os, sys
import asyncio
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

import base64
from sqlalchemy.orm import scoped_session
from db import session_factory, RandomImageTable
from eventstore import EventStore
import os
import random
import io
from seclist_payload_corpora import SeclistPayloadCorpora

class ImageCorpora:
    
    def __new__(cls, payloadCorpora: SeclistPayloadCorpora):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ImageCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self, payloadCorpora: SeclistPayloadCorpora) -> None:

        self.data = {}
        
        self.es = EventStore()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1
        
        self.payloadCorpora = payloadCorpora
    
    def load_corpora(self):
        
        if len(self.data) > 0:
            return
        
        try:
            Session = scoped_session(session_factory)
        
            rows = Session.query(RandomImageTable.c.RowNumber, RandomImageTable.c.Content).all()
            
            Session.close()
            
            for row in rows:
                
                rowDict = row._asdict()
                rn = rowDict['RowNumber']
                content = rowDict['Content']
                
                imgStrCleansed = self.removeExtraEncodedChars(content)
                
                imgByte = base64.b64decode(imgStrCleansed)

                self.data[str(rn)] = imgByte
                
            rows = None
            
        except Exception as e:
            self.es.emitErr(e)
     
    
    def removeExtraEncodedChars(self, imgStr: str):
        
        if imgStr.startswith('b\''):
            imgStr = imgStr.replace('b\'', '')
            
        if imgStr.endswith('\''):
            imgStr = imgStr[:-1]
            
        return imgStr
        
    
    def next_corpora(self):
        
        if len(self.data) == 0:
            return None
        
        randInt = random.randint(0, 10)
        
        if randInt <= 6:
            randIdx = random.randint(0, len(self.data) - 1)
            content = self.data[str(randIdx)]
            
            fBio= io.BytesIO(content)   # convert to file-like binary object
            
            fBio.seek(0)

            return fBio
        else:
            strPayload = self.payloadCorpora.next_corpora()
            
            fBio= io.BytesIO(bytes(strPayload, 'utf-8')) 
            
            fBio.seek(0)

            return fBio
                
                
        
        
    