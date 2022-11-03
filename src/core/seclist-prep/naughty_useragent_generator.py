from typing import List
from storagemanager import StorageManager
import os
import pandas as pd
import numpy as np
import sqlite3

class NaughtyUserAgentGenerator:
    
    def __init__(self, cursor) -> None:
        self.cursor = cursor
        self.sm = StorageManager()
        
    def generate_useragents(self) -> pd.DataFrame:
        
        df = self.load_naughty_useragent_from_seclist()
        df['RowNumber'] = np.arange(len(df))
        return df 
    
    def load_naughty_useragent_from_seclist(self) -> pd.DataFrame:
        
        fileNamePaths = self.sm.get_file_names_of_directory('user-agent/')
        
        if len(fileNamePaths.items) == 0:
            return []
        
        df = pd.DataFrame()
        
        RowNumber = 1
        
        for fnp in fileNamePaths:
            encodedContent = self.sm.download_file_as_str(fnp)
            
            decoded = encodedContent.decode('utf-8')
            
            splitted = decoded.split("\n")
            
            for ns in splitted:        
            
                try:
                    
                    ns = ns.replace('"', '')
                    
                    self.cursor.execute(f'''
                            insert into NaughtyUserAgent (Content, RowNumber)
                            values ("{ns}", {RowNumber})
                            ''')
                    
                    RowNumber = RowNumber + 1
                    
                except Exception as e:
                    print(e)

        
        return df
            
            
            
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
        
        
        


        