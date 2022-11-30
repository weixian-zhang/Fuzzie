from boolean_corpora import BoolCorpora
from char_corpora import CharCorpora
from datetime_corpora import DateTimeCorpora
from digit_corpora import DigitCorpora
from file_corpora import FileCorpora
from image_corpora import ImageCorpora
from password_corpora import PasswordCorpora
from pdf_corpora import PDFCorpora
from seclist_payload_corpora import SeclistPayloadCorpora
from string_corpora import StringCorpora
from username_corpora import UsernameCorpora
import asyncio

import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from utils import Utils
from eventstore import EventStore

class CorporaProvider:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CorporaProvider, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        
        self.es = EventStore()
        
        self._boolCorpora = BoolCorpora()
        self._charCorpora = CharCorpora()
        self._datetimeCorpora = DateTimeCorpora()
        self._digitCorpora = DigitCorpora()
        self._fileCorpora = FileCorpora()
        self._imageCorpora = ImageCorpora()
        self._passwordCorpora = PasswordCorpora()
        self._pdfCorpora = PDFCorpora()
        self._seclistPayloadCorpora = SeclistPayloadCorpora()
        self._stringCorpora = StringCorpora()
        self._usernameCorpora = UsernameCorpora()
        
    def load_all(self):
        try:
            self.es.emitInfo('CorporaProvider: start loading corpora')
            
            self._boolCorpora.load_corpora()
            self._charCorpora.load_corpora()
            self._datetimeCorpora.load_corpora()
            self._digitCorpora.load_corpora()
            self._fileCorpora.load_corpora()
            self._imageCorpora.load_corpora()
            self._passwordCorpora.load_corpora()
            self._pdfCorpora.load_corpora()
            self._seclistPayloadCorpora.load_corpora()
            self._stringCorpora.load_corpora()
            self._usernameCorpora.load_corpora()
            
            self.es.emitInfo('CorporaProvider: corpora fully loaded')
            
            return True, ''
            
        except Exception as e:
            self.es.emitErr(e)
            return False, Utils.errAsText(e)

        
    @property
    def boolCorpora(self):
        return self._boolCorpora
    @boolCorpora.setter
    def x(self, value):
        self._boolCorpora = value
    
    @property
    def charCorpora(self):
        return self._charCorpora
    @charCorpora.setter
    def x(self, value):
        self._charCorpora = value
    
    @property
    def datetimeCorpora(self):
        return self._datetimeCorpora
    @datetimeCorpora.setter
    def x(self, value):
        self._datetimeCorpora = value
    
    @property
    def digitCorpora(self):
        return self._digitCorpora
    @digitCorpora.setter
    def x(self, value):
        self._digitCorpora = value
    
    @property
    def fileCorpora(self):
        return self._fileCorpora
    @fileCorpora.setter
    def x(self, value):
        self._fileCorpora = value
        
    @property
    def imageCorpora(self):
        return self._imageCorpora
    @imageCorpora.setter
    def x(self, value):
        self._imageCorpora = value
    
    @property
    def passwordCorpora(self):
        return self._passwordCorpora
    @passwordCorpora.setter
    def x(self, value):
        self._passwordCorpora = value
    
    @property
    def pdfCorpora(self):
        return self._pdfCorpora
    @pdfCorpora.setter
    def x(self, value):
        self._pdfCorpora = value
    
    @property
    def seclistPayloadCorpora(self):
        return self._seclistPayloadCorpora
    @seclistPayloadCorpora.setter
    def x(self, value):
        self._seclistPayloadCorpora = value
    
    @property
    def stringCorpora(self):
        return self._stringCorpora
    @stringCorpora.setter
    def x(self, value):
        self._stringCorpora = value
    
    @property
    def usernameCorpora(self):
        return self._usernameCorpora
    @usernameCorpora.setter
    def x(self, value):
        self._usernameCorpora = value
    