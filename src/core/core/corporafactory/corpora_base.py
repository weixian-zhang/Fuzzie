class CorporaBase:
    
    def __init__(self) -> None:
        self.rowPointer = 1
        self.data = {}
        
        
    def next_corpora(self):
            
        if self.rowPointer > (len(self.data) - 1):
            self.rowPointer = 1
            
        data = self.data[str(self.rowPointer)]
        
        self.rowPointer += 1
        
        return data
    
    def reset_cursor(self, index = 1):
        self.rowPointer = 1