
from re import M
from typing import List
from storagemanager import StorageManager
import os
import pandas as pd
import base64
import numpy as np

class NaughtyFilesGenerator:
    
    def __init__(self) -> None:
        self.sm = StorageManager()
        self.blnsFileName = "blns.txt"
        self.startFolder = "payload/"
        self.folderToExclude = ["zipbombs", "max-length"]
        self.longFilenameText = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.longFilenameGif = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php.gif"
        
        
    def generate_naughty_files(self) -> pd.DataFrame:
        
        df = self.load_naughty_files_from_seclist()
        
        return df 
    
    
    def load_naughty_files_from_seclist(self) -> pd.DataFrame:
        
        fileNamePaths = self.sm.get_file_names_of_directory(self.startFolder)
        
        if len(fileNamePaths.items) == 0:
            return []
        
        df = pd.DataFrame()
        
        for fp in fileNamePaths:
            
            if self.isPartOfExcludeFolder(fp):
                continue
            
            newRow = {
                        "Filename": os.path.basename(fp),
                        "Content":  base64.b64encode(self.sm.download_file_as_bytes(fp))
                     }
            
            df = df.append(newRow, ignore_index=True,verify_integrity=False, sort=None)
            
        
        df = df.append(
                    {
                        "Filename": self.longFilenameText,
                        "Content":  ""
                     }, ignore_index=True,verify_integrity=False, sort=None)
        
        df = df.append(
                     {
                        "Filename": self.longFilenameGif,
                        "Content":  ""
                     }, ignore_index=True,verify_integrity=False, sort=None)
        
        #set running number from 1
        df['RowNumber'] = np.arange(len(df))
        
        return df
            
            
    def isPartOfExcludeFolder(self, filePath: str) -> bool:
        
        for folderToExclude in self.folderToExclude:
                
                if folderToExclude in filePath:
                    return True
                
        return False
    
    
    def isFileLongFileNameWithoutContent(self, filepath) -> bool:
        
        metadata = self.sm.get_blob_metadata(filepath)
        
        for m in metadata:
            print(m)
            pass

                
        return False
            
    
        
        
    