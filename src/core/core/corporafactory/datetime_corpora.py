from dateutil import parser
import time as tTime
from datetime import date, time, datetime
from corpora_mutator import CorporaMutator

class DateTimeCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DateTimeCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        super().__init__()
        
        self.mutator = CorporaMutator()
        
        self.timeCorpora = {}
        
        self.dateCorpora = {          }
        
    def load_corpora(self):
        self.load_date_corpora()
    
    
    def load_date_corpora(self):
        
        # '1', date.min,
        #     '2', date(1, 1, 1),
        #     '3', date(9999, 12, 31),
        #     '4', date(1904, 1, 1)  ,  #mac system
        #     '5', date(1601, 1, 1) ,   #Windows system
        #     '6', tTime.mktime(datetime.now().timetuple()), #unix timestamp
        #     '7', time(0, 0),
        #     '8', time(23, 59, 59, 999999),
        #     '9', datetime(1, 1, 1, 0, 0),
        #     '10', datetime(9999, 12, 31, 23, 59, 59, 999999),
        #     '11', datetime.now().date(),
        #     '12', datetime.now().time()
        
        dateFormats = ['%a','%A','%w','%d','%b','%B','%m','%y','%Y']
        
        dateFPerms = self.mutator.permutation(dateFormats, 0, len(dateFormats))
        
        i = 13
        for dt in dateFPerms:
            strFormat =  " ".join(dt)
            dtVal = datetime.now().strftime(strFormat)
            self.dateCorpora[str(i)] = dtVal
            
            i = i + 1
        