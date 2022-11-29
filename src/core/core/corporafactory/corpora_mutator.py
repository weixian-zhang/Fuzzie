
from char_corpora import CharCorpora
import random

import os, sys
from pathlib import Path
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
from eventstore import EventStore

class CorporaMutator:
    
    def __init__(self) -> None:
        
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
        
        data = []
        
        for x in range(0, len(text) * setSize):
            
           mutated = self.randomStrategy()(text)
            
           data.append(mutated)
            
            
        return data
    
    def mutate_list(self, listText: list[str], setSize=4):
        
        if listText is None or len(listText) == 0:
            self.es.emitErr(Exception(f'no input to mutate for expression {listText}'))
            return []
        
        data = []
        
        for t in listText:
            mutated = self.mutate_single(t, setSize=setSize)
            data = data + mutated
            
        return data
        
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
    
    
    def permutation(self, items : list[str], index, length):
        

        def swap(arr, fIdx, sIdx):
            newArr = arr.copy()
            temp = newArr[fIdx]
            newArr[fIdx] = newArr[sIdx]
            newArr[sIdx] = temp
            return newArr
    
        def permute(arr, index, length, result: list):
             
            if index == length:
                result.append(arr.copy())
            else:
            
                for i in range(index, length + 1):
                    
                    newArr = swap(arr, index, i)
                    permute(newArr, index + 1, length, result)
                    newArr = swap(arr, index, i)

            
        result = []
        permute(items, index, length - 1, result)
        return result
        

    
    def combinations(self, strs : list[str]):
        pass