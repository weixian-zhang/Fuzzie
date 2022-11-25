
from corpora_base import CorporaBase
from char_corpora import CharCorpora
import random

import os, sys
from pathlib import Path
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
from eventstore import EventStore

class CorporaMutator(CorporaBase):
    
    def __init__(self) -> None:
        
        super().__init__()
        
        self.runningNumber = 0
        
        self.charC = CharCorpora()
        self.es = EventStore()
        
        self.mutationStrategies = {
            0: self.replace,
            1: self.append,
            2: self.reduce,
            3: self.swap
            }
        
    # setSize is the number of times to mutate a text
    def mutate_single(self, text: str, setSize=4):
        
        for x in range(0, len(text) * setSize):
            
            mutated = self.randomStrategy()(text)
            
            self.data[str(self.runningNumber)] = mutated
            
            self.runningNumber = self.runningNumber  + 1
    
    def mutate_list(self, listText: list[str]):
        
        if str is None or len(str) == 0:
            self.es.emitErr(Exception(f'no input to mutate for expression {listText}'))
            return []
        
        for t in listText:
            self.mutate_single(t)
        
    def replace(self, text):
       chars = list(text)
        
       index = random.randint(0, len(text) - 1)
       
       chars[index] = self.charC.next_corpora()
       
       return "".join(chars)
    
    def append(self, text):
        
        idx = random.randint(0, len(text) - 1)
        
        charToAdd = self.charC.next_corpora()
        
        newText = text[:idx] + charToAdd + text[idx:]
        
        return newText
        
    
    def reduce(self, text):
        idx = random.randint(0, len(text) - 1)
        chars = list(text)
        chars[idx] = ''
        return "".join(chars)
    
    def swap(self, text):
        if len(text) == 1:
            return self.replace(text)
        
        firstInd = random.randint(0, len(text) - 1)
        secondInd = random.randint(0, len(text) - 1)
        
        # ensure both index is differernt
        while secondInd == firstInd:
            secondInd = random.randint(0, len(text) -1)
            
        f = text[firstInd]
        
        s= text[secondInd]
        
        chars = list(text)
        
        chars[firstInd] = s
        
        chars[secondInd] = f
        
        return "".join(chars)
    
    def randomStrategy(self):
        rand = random.randint(0, 3)
        return self.mutationStrategies[rand]