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

        self.data = {}
        
        self.es = EventStore()
        
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
        
    def next_corpora(self):
        
        try:
            tpl = jinja2.Template(self.myfileContentExpr)
            output = tpl.render({ 'eval': self.resolve_primitive_wordlist_types })
            return output
        
        except Exception as e:
            self.es.emitErr(e)
            return self.stringCorpora.next_corpora()
        
        
    def resolve_primitive_wordlist_types(self, wordlist_type = 'string'):
        
        data = ''
        
        match wordlist_type:
            case 'string':
                data = self.stringCorpora.next_corpora()
            case 'bool':
                data = self.boolCorpora.next_corpora()
            case 'digit':
                data = self.digitCorpora.next_corpora()
            case 'char':
                data = self.charCorpora.next_corpora()
            case 'filename':
                data = self.filenameCorpora.next_corpora()
            case 'datetime':
                data = self.datetimeCorpora.next_corpora()
            case 'date':
                data = self.datetimeCorpora.next_date_corpora()
            case 'time':
                data = self.datetimeCorpora.next_time_corpora()
            case 'username':
               data = self.usernameCorpora.next_corpora()
            case 'password':
                data = self.passwordCorpora.next_corpora()
            case _:
                data = self.stringCorpora.next_corpora()
                
        return data
        
        