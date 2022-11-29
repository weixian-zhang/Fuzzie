
from corpora_mutator import CorporaMutator
import random

# this corpora provider cannot be singleton as there can be more than one user-supplied expressions
class UserSuppliedCorpora:
    
    def __init__(self) -> None:
        
        self.dataCursor = 1
        
        self.data = []
        
        self.mutator = CorporaMutator()
        
    
    def load_corpora(self, value):
        
        if isinstance(value, list):
            mutated = self.mutator.mutate_list(value, setSize=5)
        
            self.data = self.data + mutated
        else:
            mutated = self.mutator.mutate_single(value, setSize=5)
        
            self.data = self.data + mutated
                
        
    def next_corpora(self):
        
        randIdx = random.randint(0, len(self.data) - 1)
        
        data = self.data[randIdx]
        
        self.dataCursor = self.dataCursor + 1
                         
        return data