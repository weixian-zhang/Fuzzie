import os, sys
import asyncio
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from boolean_corpora import BoolCorpora
from char_corpora import CharCorpora
from datetime_corpora import DateTimeCorpora
from digit_corpora import DigitCorpora
from image_corpora import ImageCorpora
from password_corpora import PasswordCorpora
from pdf_corpora import PDFCorpora
from seclist_payload_corpora import SeclistPayloadCorpora
from string_corpora import StringCorpora
from username_corpora import UsernameCorpora
from filename_corpora import FileNameCorpora
from sqlalchemy.orm import scoped_session
from db import session_factory, SeclistPasswordTable
from eventstore import EventStore
import os
import jinja2

# MyFileCorpora is not a singleton object, each myfile expression commands a dedicated object instance
# MyFileCorpora only supports primitive corpora types as declared in constructor
class MyFileCorpora:
    
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(MyFileCorpora, cls).__new__(cls)
    #     return cls.instance
    
    def __init__(self, myfileContentExpr: str, 
                 boolCorpora, 
                 charCorpora,
                 datetimeCorpora,
                 digitCorpora,
                 passwordCorpora,
                 stringCorpora,
                 usernameCorpora,
                 filenameCorpora
                 ) -> None:
        self.rowPointer = 0
        self.data = {}
        
        self.es = EventStore()
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1
        
        self.myfileContentExpr = myfileContentExpr
        self.boolCorpora = boolCorpora
        self.charCorpora = charCorpora
        self.datetimeCorpora =datetimeCorpora
        self.digitCorpora = digitCorpora
        self.passwordCorpora = passwordCorpora
        self.stringCorpora = stringCorpora
        self.usernameCorpora = usernameCorpora
        self.filenameCorpora = filenameCorpora
    
    # exist as contract similar to all corpora class
    def load_corpora(self, myfileContentExpr: str):
        pass
        #self.myfileContentExpr = myfileContentExpr  
        
    def next_corpora(self):
        
        tpl = jinja2.Template(self.myfileContentExpr)
            
        output = tpl.render(
            {
                'string': self.stringCorpora.next_corpora(),
                'bool':  self.boolCorpora.next_corpora(),
                'digit': self.corporaProvider.digitCorpora.next_corpora(),
                'char':self.charCorpora.next_corpora(),
                'filename': self.filenameCorpora.next_corpora(),
                'datetime': self.datetimeCorpora.next_corpora(),
                'date': self.datetimeCorpora.next_date_corpora(),
                'time': self.datetimeCorpora.next_time_corpora(),
                'username': self.usernameCorpora.next_corpora(),
                'password': self.filenameCorpora.next_corpora()
            })
        
        return output