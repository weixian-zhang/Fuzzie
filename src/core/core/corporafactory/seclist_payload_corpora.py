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
from db import session_factory, SeclistPayloadTable
from eventstore import EventStore
import os

class SeclistPayloadCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SeclistPayloadCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        self.rowPointer = 1
        self.data = {}
        
        self.es = EventStore()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1
        
    def load_corpora(self):
        try:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.create_task(self.load_corpora_async())
            ]
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception as e:
            self.es.emitErr(e)
            
    def load_corpora_async(self):
        
        if len(self.data) > 0:
            return
        
        Session = scoped_session(session_factory)
        
        rows = Session.query(SeclistPayloadTable.c.RowNumber, SeclistPayloadTable.c.Filename, SeclistPayloadTable.c.Content).all()
        
        Session.close()
        
        for row in rows:
            
            rowDict = row._asdict()
            rn = rowDict['RowNumber']
            filename = rowDict['Filename']
            content = rowDict['Content']
            
            self.data[str(rn)] = {'filename': filename, 'content': content}
            
        rows = None
        
    def next_corpora(self):
        
        try:
            if self.rowPointer > (len(self.data) - 1):
                self.rowPointer = 1
            
            fileCor = self.data[str(self.rowPointer)]

            content = fileCor['content']
            content = self.removeExtraEncodedChars(content)
            content = base64.b64decode(content)
            
            self.rowPointer += 1
            
            return content
        
        except Exception as e:
            self.es.emitErr(e, 'SeclistPayloadCorpora.next_corpora')
            
    
    def removeExtraEncodedChars(self, imgStr: str):
        
        if imgStr.startswith('b\''):
            imgStr = imgStr.replace('b\'', '')
            
        if imgStr.endswith('\''):
            imgStr = imgStr[:-1]
            
        return imgStr
        
        
        