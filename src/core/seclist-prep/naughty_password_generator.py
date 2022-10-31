from typing import List
from storagemanager import StorageManager
import os
import pandas as pd
import numpy as np

class NaughtyPasswordGenerator:
    
    def __init__(self, cursor) -> None:
        self.cursor = cursor
        self.sm = StorageManager()
        
    def generate_naughty_password(self):
        
        self.download_password_from_seclist()
    
    def download_password_from_seclist(self) -> pd.DataFrame:
        
        fileNamePaths = self.sm.get_file_names_of_directory('password/')
        
        if len(fileNamePaths.items) == 0:
            return []
        
        df = pd.DataFrame()
        
        for fnp in fileNamePaths:
            encodedContent = self.sm.download_file_as_str(fnp)
            
            decoded = encodedContent.decode('utf-8')
            
            splitted = decoded.split("\n")
                
            
            RowNumber = 1
            
            for ns in splitted:        
                    try:
                                                
                        ns = ns.replace('"', '')
                        
                        self.cursor.execute(f'''
                                insert into NaughtyPassword(Content, RowNumber)
                                values ("{ns}", {RowNumber})
                                ''')
                        
                        RowNumber = RowNumber + 1
                        
                    except Exception as e:
                        print(e)
    