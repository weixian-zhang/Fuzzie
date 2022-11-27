from password_corpora import PasswordCorpora
from username_corpora import UsernameCorpora
from corpora_mutator import CorporaMutator
    

class CorporaProvider:
    
    def __init__(self) -> None:
        
        self.passwordCorpora = PasswordCorpora()
        self.usernameCorpora = UsernameCorpora()
        self.blnsCorpora = ''
        self.corporaMutator = CorporaMutator()
        
    def load_all(self):
        self.passwordCorpora.load_corpora()
        
    @property
    def passwordCorpora(self):
        return self.passwordCorpora
    
    @property
    def blnsCorpora(self):
        return self.passwordCorpora
    