import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

import string
import random
import uuid
import datetime

class NumberRangeCorpora:
        
    def __init__(self, start=1, end=80000) -> None:
        
        self.start = start
        self.end = end
        self.data = {}
        self.dataLimit = 80000  #limit number range no matter how large the range is
        
        self.rowPointer = 0; #important as sqlite autoincrement id starts from 1, pt-dict starts from 0

    
    def load_corpora(self):
        
        if len(self.data) > 0:
            return
        
        if self.start >= self.end:
            self.start = 1
            self.end = self.dataLimit
        
        for i in range(self.start, self.end):
            if i >= self.dataLimit:
                return
            
            self.data[self.rowPointer] = i
            self.rowPointer = self.rowPointer + 1
            
        self.rowPointer = 0 #reset pointer
            
        
    def next_corpora(self):
        
        if self.rowPointer >= len(self.data):
            self.rowPointer = 0
            
        data = self.data[self.rowPointer]
        
        self.rowPointer = self.rowPointer + 1
        
        return data
        
        