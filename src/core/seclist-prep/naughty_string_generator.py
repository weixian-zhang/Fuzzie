from typing import List
from storagemanager import StorageManager
import os
import pandas as pd
import numpy as np

class NaughtyStringGenerator:
    
    def __init__(self, cursor) -> None:
        self.cursor = cursor
        self.sm = StorageManager()
        self.blnsFileName = "blns.txt"
        
    def generate_naughty_strings(self) -> pd.DataFrame:
        
        df = self.load_naughty_strings_from_seclist()
        df['RowNumber'] = np.arange(len(df))
        return df 
    
    def load_naughty_strings_from_seclist(self) -> pd.DataFrame:
        
        fileNamePaths = self.sm.get_file_names_of_directory('naughty-strings/')
        
        if len(fileNamePaths.items) == 0:
            return []
        
        df = pd.DataFrame()
        
        RowNumber = 1
        
        for fnp in fileNamePaths:
            try:
                
                encodedContent = self.sm.download_file_as_str(fnp)
                
                decoded = encodedContent.decode('utf-8')
                
                splitted = []
                
                if self.is_blns_file(fnp):
                    splitted = self.handle_blns_content_splitting(decoded)
                else:
                    splitted = decoded.split("\n")
                    
                for ns in splitted:        
                
                        if ns.startswith('#'):
                            continue
                        
                        ns = ns.replace('"', '')
                        
                        self.cursor.execute(f'''
                                insert into NaughtyString (Content, RowNumber)
                                values ("{ns}", {RowNumber})
                                ''')
                        
                        RowNumber = RowNumber + 1
                    
            except Exception as e:
                print(e)
        
            # for ns in splitted:
            #     newRow = { "Content": ns }
            #     df = df.append(newRow, ignore_index=True,verify_integrity=False, sort=None)
        
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
        
        
        


        