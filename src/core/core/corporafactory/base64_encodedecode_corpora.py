import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)
import json
import base64
from utils import Utils
import random

list_delimiter = '```'

class Base64EncodeCorpora:
        
    def __init__(self, value: any) -> None:
        
        # for single string, list contains 1 item
        valueArr = value.split(list_delimiter)
        
        self.data = valueArr
    
    def load_corpora(self):
        pass
            
        
    def next_corpora(self):
        
        listItemVal = ''
        
        try:
            
            if len(self.data) == 0:
                return ''
            
            randIdx = random.randint(0, len(self.data) - 1)
                
            listItemVal = self.data[randIdx]
            
            if listItemVal == '':
                return ''
            
            b64e = Utils.b64e(listItemVal) 
            
            return b64e
    
        except Exception as e:
            return listItemVal
        
class Base64DecodeCorpora:
        
    def __init__(self, value: str) -> None:
        
        # for single string, list contains 1 item
        valueArr = value.split(list_delimiter)
        
        self.data = valueArr
    
    def load_corpora(self):
        pass
            
        
    def next_corpora(self):
        
        listItemVal = ''
        
        try:
            
            if len(self.data) == 0:
                return ''
            
            randIdx = random.randint(0, len(self.data) - 1)
                
            listItemVal = self.data[randIdx]
            
            if listItemVal == '':
                return ''
            
            b64d = Utils.b64d(listItemVal) 
            
            return b64d
            
        except Exception as e:
            return listItemVal
    
        
        
        
        