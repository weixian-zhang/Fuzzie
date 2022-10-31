from typing import List
from storagemanager import StorageManager
import os
import pandas as pd
import numpy as np

class NaughtyUsernameGenerator:
    
    def __init__(self, cursor) -> None:
        self.cursor = cursor
        self.sm = StorageManager()
        
    def generate_naughty_usernames(self) -> pd.DataFrame:
        
        self.download_usernames_from_seclist()
    
    def download_usernames_from_seclist(self):
        
        fileNamePaths = self.sm.get_file_names_of_directory('usernames/')
        
        if len(fileNamePaths.items) == 0:
            return []
        
        for fnp in fileNamePaths:
            encodedContent = self.sm.download_file_as_str(fnp)
            
            decoded = encodedContent.decode('utf-8')
            
            splitted = decoded.split("\n")
            
            RowNumber = 1
            
            for ns in splitted:        
                    try:
                        
                        ns = ns.replace('"', '')
                        
                        self.cursor.execute(f'''
                                insert into NaughtyUsername(Content, RowNumber)
                                values ("{ns}", {RowNumber})
                                ''')
                        
                        RowNumber = RowNumber + 1
                        
                    except Exception as e:
                        print(e)
                
            
            # for ns in splitted:
            #     newRow = { "Content": ns }
            #     df = df.append(newRow, ignore_index=True,verify_integrity=False, sort=None)