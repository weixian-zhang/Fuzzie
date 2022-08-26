from typing import List
from storagemanager import StorageManager
import os
import pandas as pd

class NaughtyStringGenerator:
    
    def __init__(self) -> None:
        self.sm = StorageManager()
        self.blnsFileName = "blns.txt"
        
    def generate_naughty_strings(self) -> pd.DataFrame:
        
        naughtyStrings = self.load_naughty_strings_from_seclist()
        df = pd.DataFrame()
        df['naughtystrings'] = naughtyStrings
        return df 
    
    def load_naughty_strings_from_seclist(self) -> List:
        
        fileNamePaths = self.sm.get_file_names_of_directory('naughty-strings/')
        
        if len(fileNamePaths) == 0:
            return []
        
        merged = []
        
        for fnp in fileNamePaths:
            encodedContent = self.sm.download_file_as_str(fnp)
            
            decoded = encodedContent.decode('utf-8')
            
            splitted = []
            
            if self.is_blns_file(fnp):
                splitted = self.handle_blns_content_splitting(decoded)
            else:
                splitted = decoded.split("\n")
            
            merged += splitted
            
        return merged
            
            
            
    def is_blns_file(self, fileNamePath):
        
        if os.path.basename(fileNamePath) == self.blnsFileName:
            return True
        return False
            
    def handle_blns_content_splitting(self, content):
        splitted = content.split("\r\n")
        
        # remove comments and empty strings in seclist
        cleansed = [x for x in splitted if not x.startswith('#') and not x == ""] 
        
        return cleansed
        
        
    
    def handle_seclist_content_splitting(self):
        pass
        
        
        
    
        
        