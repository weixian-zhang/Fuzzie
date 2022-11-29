from dateutil import parser
import time as tTime
from datetime import date, time, datetime
from dateutil import parser
import datetime
from corpora_mutator import CorporaMutator
import random

import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)

from eventstore import EventStore


class DateTimeCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DateTimeCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        super().__init__()
        
        self.dateCursor = 1
        self.timeCursor = 1
        
        self.es = EventStore()
        
        self.mutator = CorporaMutator()
        
        self.timeCorpora = {}
        
        self.dateCorpora = {}
        
    def load_corpora(self):
        
        if len(self.timeCorpora) > 0 and len(self.dateCorpora) > 0:
            return
        
        self.load_date_corpora()
        self.load_time_corpora()
    
    
    def load_date_corpora(self):
        
        try:
            self.dateCorpora['1'] = date.min
            self.dateCorpora['2'] = date(1, 1, 1)
            self.dateCorpora['3'] = date(9999, 12, 31)
            self.dateCorpora['4'] = date(1601, 1, 1)
            self.dateCorpora['5'] = tTime.mktime(datetime.datetime.now().timetuple())
            self.dateCorpora['6'] = time(0, 0)
            self.dateCorpora['7'] = time(23, 59, 59, 999999)
            self.dateCorpora['8'] = datetime.datetime(1, 1, 1, 0, 0)
            self.dateCorpora['9'] = datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)
            self.dateCorpora['10'] = datetime.datetime.now().date()
            self.dateCorpora['11'] = datetime.datetime.now().time()
            
            dateFormats = ['%a','%A','%w','%d','%b','%B','%m','%y']
            
            dateFPerms = self.mutator.permutation(dateFormats, 0, len(dateFormats))
            
            i = 12
            for dt in dateFPerms:
                strFormat =  " ".join(dt)
                
                randYear = random.randrange(1900, 2100)
                randMth = random.randrange(1, 12)
                randDay = random.randrange(1, 31)
                
                try:
                    dtVal = datetime.datetime(randYear, randMth, randDay).strftime(strFormat)
                except:
                    # error thrown for day out-of-range fro certain months without 29/30/31
                    continue
                
                self.dateCorpora[str(i)] = dtVal
                
                i = i + 1
        except Exception as e:
            self.es.emitErr(e)
            
    def load_time_corpora(self):
        
        try:
            i = 1
            
            timeFormats = ['%H','%I','%p','%M','%S','%f']
        
            timeFPerms = self.mutator.permutation(timeFormats, 0, len(timeFormats))
            
            for t in timeFPerms:
                
                randYear = random.randrange(1900, 2100)
                randMth = random.randrange(1, 12)
                randDay = random.randrange(1, 31)
                randH = random.randrange(1, 12)
                randM = random.randrange(1, 59)
                randSec = random.randrange(1, 59)
                
                strFormat =  " ".join(t)
                
                tVal = datetime.datetime(randYear, randMth, randDay, randH, randM, randSec).strftime(strFormat)
                
                self.timeCorpora[str(i)] = tVal
                
                i = i + 1

        except Exception as e:
            self.es.emitErr(e)
        
       
            
    
    def next_date_corpora(self):
            
        if self.dateCursor > (len(self.dateCorpora) - 1):
            self.dateCursor = 1
            
        data = self.dateCorpora[str(self.dateCursor)]
        
        self.dateCursor += 1
        
        return data
    
    def next_time_corpora(self):
            
        if self.timeCursor > (len(self.timeCorpora) - 1):
            self.timeCursor = 1
            
        data = self.timeCorpora[str(self.timeCursor)]
        
        self.timeCursor += 1
        
        return data
    
    def next_datetime_corpora(self):
            
        d = self.next_date_corpora()
        t = self.next_time_corpora()
        return f'{d} {t}'
        
        
        