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

class CorporaProvider:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CorporaProvider, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        
        self.boolCorpora = BoolCorpora()
        self.charCorpora = CharCorpora()
        self.datetimeCorpora = DateTimeCorpora()
        self.digitCorpora = DigitCorpora()
        self.imageCorpora = ImageCorpora()
        self.passwordCorpora = PasswordCorpora()
        self.pdfCorpora = PDFCorpora()
        self.seclistPayloadCorpora = SeclistPayloadCorpora()
        self.stringCorpora = StringCorpora()
        self.usernameCorpora = UsernameCorpora()
        
    def load_all(self):
        self.boolCorpora.load_corpora()
        self.charCorpora.load_corpora()
        self.digitCorpora.load_corpora()
        self.digitCorpora.load_corpora()
        self.imageCorpora.load_corpora()
        self.passwordCorpora.load_corpora()
        self.pdfCorpora.load_corpora()
        self.seclistPayloadCorpora.load_corpora()
        self.stringCorpora.load_corpora()
        self.usernameCorpora.load_corpora()
        
    @property
    def boolCorpora(self):
        return self.boolCorpora
    
    @property
    def charCorpora(self):
        return self.charCorpora
    
    @property
    def datetimeCorpora(self):
        return self.datetimeCorpora
    
    @property
    def digitCorpora(self):
        return self.digitCorpora
    
    @property
    def imageCorpora(self):
        return self.imageCorpora
    
    @property
    def passwordCorpora(self):
        return self.passwordCorpora
    
    @property
    def pdfCorpora(self):
        return self.pdfCorpora
    
    @property
    def seclistPayloadCorpora(self):
        return self.seclistPayloadCorpora
    
    @property
    def stringCorpora(self):
        return self.stringCorpora
    
    @property
    def userSuppliedCorpora(self) -> Usersu:
        return self.userSuppliedCorpora
    
    @property
    def usernameCorpora(self):
        return self.usernameCorpora
    