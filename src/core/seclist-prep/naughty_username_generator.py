from typing import List
from storagemanager import StorageManager
import os
import pandas as pd
import numpy as np

class NaughtyUsernameGenerator:
    
    def __init__(self) -> None:
        self.sm = StorageManager()
        
    def generate_naughty_usernames(self) -> pd.DataFrame:
        
        df = self.download_usernames_from_seclist()
        df['RowNumber'] = np.arange(len(df))
        return df 
    
    def download_usernames_from_seclist(self) -> pd.DataFrame:
        
        fileNamePaths = self.sm.get_file_names_of_directory('usernames/')
        
        if len(fileNamePaths.items) == 0:
            return []
        
        df = pd.DataFrame()
        
        for fnp in fileNamePaths:
            encodedContent = self.sm.download_file_as_str(fnp)
            
            decoded = encodedContent.decode('utf-8')
            
            splitted = decoded.split("\n")
                
            
            for ns in splitted:
                newRow = { "Content": ns }
                df = df.append(newRow, ignore_index=True,verify_integrity=False, sort=None)
        
        return df