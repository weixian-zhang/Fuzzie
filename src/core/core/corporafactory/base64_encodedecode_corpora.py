import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

import base64

class Base64EncodeCorpora:
        
    def __init__(self, value: str) -> None:
        
        self.data = value
    
    def load_corpora(self):
        pass
            
        
    def next_corpora(self):
        
        if not self.data or self.data == '':
            return ''
        
        try:
            valBytes = self.data.encode('utf-8')
        
            encoded = base64.b64encode(valBytes)
            
            b64Str = encoded.decode('utf-8')
            
            return b64Str
    
        except Exception as e:
            return ''
        
class Base64DecodeCorpora:
        
    def __init__(self, value: str) -> None:
        
        self.data = value
    
    def load_corpora(self):
        pass
            
        
    def next_corpora(self):
        
        if not self.data or self.data == '':
            return ''
        
        try:
            b64Bytes = self.data.encode('utf-8')
            
            strBytes = base64.b64decode(b64Bytes)
            
            valStr = strBytes.decode('utf-8')
            
            return valStr
            
        except Exception as e:
            return ''
    
        
        
        
        