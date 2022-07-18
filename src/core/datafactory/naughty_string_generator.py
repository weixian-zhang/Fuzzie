from typing import List
from storagemanager import StorageManager
import pandas as pd
import json

class NaughtyStringGenerator:
    
    def __init__(self) -> None:
        self.sm = StorageManager()
        
    def get_naughty_strings(self) -> pd.DataFrame:
        
        blns = self.get_blns()
        
        xss = self.get_xss_strings()
        
        merged = blns + xss
        
        return merged 
    
    
    def get_blns(self) -> List:
        
        try:
        
            blnsJson = self.sm.download_file_as_str('blns.txt', 'naughty-strings')
            
            decoded =  blnsJson.decode("utf-8") 
            
            strList = decoded.split("\r\n")
            
            nsList = [s for s in strList if not s.startswith("#")] #ignore comments in blns.txt
            
            return nsList
        
        except Exception as e:
            # log with loguru
            raise
    
    def get_xss_strings(self) -> List:
        
        try:
            brutelogicBinary = self.sm.download_file_as_str('XSS-BruteLogic.txt', 'naughty-strings', 'xss')
            
            blDecoded =  brutelogicBinary.decode("utf-8")
            
            blStrList = blDecoded.split("\n")
            
            return blStrList
        
        except Exception as e:
            # log with loguru
            raise
        
        