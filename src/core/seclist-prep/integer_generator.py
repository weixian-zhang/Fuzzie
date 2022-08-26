from storagemanager import StorageManager
import pandas as pd
import os
from data_factory_utils import DataFactoryUtils

# integer data requirements
# Seclist already contains various positive/negative integer data and a large 4MB interger
# self generate 
    # prepend 0s
# repeat data base on number of records in naughty_strings
class IntegerGenerator:
    
    def __init__(self):
        
        self.sm = StorageManager()
        self.piLargerIntegerFileName = 'pi-large.txt'
    
    def generate_integers(self, noOfRowsToPad = 1000) -> list:
        
        # data contains some floats
        intData = DataFactoryUtils.load_bad_integers_from_seclist()
        
        if noOfRowsToPad <= len(intData):
            return intData
        
        rowsExcludeSuperLargeInt = noOfRowsToPad - 1
        
        dupList = DataFactoryUtils.pad_rows(intData, rowsExcludeSuperLargeInt)
        
        # prepend super large int only once in the list to prevent taking up too much memory as 1 large integer is 4MB
        superLargeInt = self.load_superlarge_integer_from_seclist()
        dupList.insert(0, superLargeInt)

        return dupList    
    
    def load_superlarge_integer_from_seclist(self):
        
        #filePath = self.sm.get_file_names_of_directory()
        content = self.sm.download_file_as_str('digit/pi-large.txt')
        decoded = content.decode('utf-8')
        return decoded
    
    