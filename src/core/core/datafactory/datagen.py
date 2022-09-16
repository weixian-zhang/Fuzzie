

class DataGenerator:
    
    def __init__(self) -> None:
        self.rowPointer = 0
        self.data = []
        
        
    def NextData(self):
            
        if self.rowPointer > (len(self.data) - 1):
            self.rowPointer = 0
            
        data = self.data[self.rowPointer]
        
        self.rowPointer += 1
        
        return data