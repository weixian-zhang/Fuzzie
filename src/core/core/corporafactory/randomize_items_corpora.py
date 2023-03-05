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

class RandomItemsCorpora:
        
    def __init__(self, items: list[any]) -> None:
        
        self.data = items
    
    #nothing to load as data s supplied by user
    def load_corpora(self):
        pass
            
        
    def next_corpora(self):
        
        if len(self.data) == 0:
            return ''
        
        endInx = len(self.data) - 1
        
        randIdx = random.randint(0, endInx)
        
        return self.data[randIdx]
        
        