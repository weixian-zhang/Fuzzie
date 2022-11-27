

class BoolCorpora:
    
    def __init__(self) -> None:
        self.rowPointer = 0
        self.data = [True, False, None, 0, 1, 'true', 'false', 'yes', 'no', '1', '0', 't', 'f', 'T', 'F', 'TRUE', 'FALSE', '', None]
            
        
    def next_corpora(self):
            
        if self.rowPointer > (len(self.data) - 1):
            self.rowPointer = 0
            
        data = self.data[self.rowPointer]
        
        self.rowPointer += 1
        
        return data