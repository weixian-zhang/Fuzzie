import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

from db import engine
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
from myfile_corpora_provider import MyFileCorpora

from pubsub import pub

from utils import Utils
from eventstore import EventStore

class CorporaProvider:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CorporaProvider, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        
        # if CorporaProvider.hasExistingInstance == True:
        #     return
        
        self.es = EventStore()
        
        self._boolCorpora = BoolCorpora()
        self._charCorpora = CharCorpora()
        self._datetimeCorpora = DateTimeCorpora()
        self._digitCorpora = DigitCorpora()
        self._passwordCorpora = PasswordCorpora()
        self._seclistPayloadCorpora = SeclistPayloadCorpora()
        self._imageCorpora = ImageCorpora(self._seclistPayloadCorpora)
        self._pdfCorpora = PDFCorpora(self._seclistPayloadCorpora)
        self._stringCorpora = StringCorpora()
        self._usernameCorpora = UsernameCorpora()
        self._filenameCorpora = FileNameCorpora()
    
    def load_files_corpora(self):
        #self.es.emitInfo('CorporaProvider: loading payload corpora')
        self._seclistPayloadCorpora.load_corpora()
        self.es.emitInfo('CorporaProvider: payload corpora loaded')
        
        #self.es.emitInfo('CorporaProvider: loading pdf corpora')
        self._pdfCorpora.load_corpora()
        self.es.emitInfo('CorporaProvider: pdf corpora loaded')
        
        self._imageCorpora.load_corpora()
        self.es.emitInfo('CorporaProvider: image corpora loaded')
        
    def load_username_corpora(self):
        
        self._usernameCorpora.load_corpora()
        self.es.emitInfo('CorporaProvider: username corpora loaded')
        
    def load_password_corpora(self):
        self._passwordCorpora.load_corpora()
        self.es.emitInfo('CorporaProvider: password corpora loaded')
        
    def load_string_corpora(self):
        self._stringCorpora.load_corpora()
        self.es.emitInfo('CorporaProvider: string corpora loaded')
        
    def vacuumSqlite(self):
        self.es.emitInfo('vacuuming sqlite')
        engine.execute("VACUUM")
        self.es.emitInfo('sqlite vacuumed')
        
    def load_all(self):
        try:
            
            self.es.emitInfo('vacuuming sqlite')
            engine.execute("VACUUM")
            self.es.emitInfo('sqlite vacuumed')
            

            self.es.emitInfo('CorporaProvider: start loading corpora')

            #self.es.emitInfo('CorporaProvider: loading boolean corpora')
            self._boolCorpora.load_corpora()
            self.es.emitInfo('CorporaProvider: boolean corpora loaded')
            
            #self.es.emitInfo('CorporaProvider: loading char corpora')
            self._charCorpora.load_corpora()
            self.es.emitInfo('CorporaProvider: char corpora loaded')
            
            #self.es.emitInfo('CorporaProvider: loading datetime corpora')
            self._datetimeCorpora.load_corpora()
            self.es.emitInfo('CorporaProvider: datetime corpora loaded')
            
            #self.es.emitInfo('CorporaProvider: loading digit corpora')
            self._digitCorpora.load_corpora()
            self.es.emitInfo('CorporaProvider: digit corpora loaded')
            
            #self.es.emitInfo('CorporaProvider: loading image corpora')
            # self._imageCorpora.load_corpora()
            # self.es.emitInfo('CorporaProvider: image corpora loaded')
            
            #self.es.emitInfo('CorporaProvider: loading password corpora')
            # self._passwordCorpora.load_corpora()
            # self.es.emitInfo('CorporaProvider: password corpora loaded')
            
            # #self.es.emitInfo('CorporaProvider: loading pdf corpora')
            # self._pdfCorpora.load_corpora()
            # self.es.emitInfo('CorporaProvider: pdf corpora loaded')
            
            # #self.es.emitInfo('CorporaProvider: loading payload corpora')
            # self._seclistPayloadCorpora.load_corpora()
            # self.es.emitInfo('CorporaProvider: payload corpora loaded')
            
            #self.es.emitInfo('CorporaProvider: loading string corpora')
            self._stringCorpora.load_corpora()
            self.es.emitInfo('CorporaProvider: string corpora loaded')
            
            #self.es.emitInfo('CorporaProvider: loading username corpora')
            # self._usernameCorpora.load_corpora()
            # self.es.emitInfo('CorporaProvider: username corpora loaded')
            
            #self.es.emitInfo('CorporaProvider: loading file corpora')
            self._filenameCorpora.load_corpora()
            self.es.emitInfo('CorporaProvider: file corpora loaded')
            
            self.es.emitInfo('CorporaProvider: corpora fully loaded')
            
            return True, ''
            
        except Exception as e:
            errText = Utils.errAsText(e)
            pub.sendMessage(topicName=self.es.CorporaEventTopic, command='corpora_load_error', msgData=errText)
            self.es.emitErr(errText)
            return False, errText
        
    def new_myfile_corpora(self, myfileContentExpr: str):
        myfilec = MyFileCorpora(myfileContentExpr, 
                                boolCorpora=self._boolCorpora,
                                charCorpora = self._charCorpora,
                                datetimeCorpora = self._datetimeCorpora,
                                digitCorpora = self._digitCorpora,
                                passwordCorpora = self._passwordCorpora,
                                stringCorpora = self._stringCorpora,
                                usernameCorpora = self._usernameCorpora,
                                filenameCorpora = self._filenameCorpora)
        return myfilec
        

    # @property
    # def myfileCorpora(self):
    #     return self._myfileCorpora
    # @myfileCorpora.setter
    # def x(self, value):
    #     self._myfileCorpora = value
        
    @property
    def fileNameCorpora(self):
        return self._filenameCorpora
    @fileNameCorpora.setter
    def x(self, value):
        self._filenameCorpora = value
        
    @property
    def fileCorpora(self):
        return self._fileCorpora
    @fileCorpora.setter
    def x(self, value):
        self._fileCorpora = value
        
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
    