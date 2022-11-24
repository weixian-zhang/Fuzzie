from password_corpora import PasswordCorpora
from username_corpora import UsernameCorpora
from corporal_mutator import CorporaMutator

class CorporaBase:
    
    def __init__(self) -> None:
        self.rowPointer = 0
        self.data = []
        
        
    def next_corpora(self):
            
        if self.rowPointer > (len(self.data) - 1):
            self.rowPointer = 0
            
        data = self.data[self.rowPointer]
        
        self.rowPointer += 1
        
        return data
    

class CorporaProvider:
    
    def __init__(self) -> None:
        
        self.passwordCorpora = PasswordCorpora()
        self.usernameCorpora = UsernameCorpora()
        self.blnsCorpora = ''
        self.corporaMutator = CorporaMutator()
        
    def load_corpora(self):
        self.passwordCorpora.load_corpora()
        
    @property
    def passwordCorpora(self):
        return self.passwordCorpora
    
    @property
    def blnsCorpora(self):
        return self.passwordCorpora
    