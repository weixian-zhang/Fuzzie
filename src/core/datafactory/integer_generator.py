from storagemanager import StorageManager
import pandas as pd
import os
from utils_list import ListUtils

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
        
        intData = self.load_integers_from_seclist()
        
        dupList = ListUtils.pad_rows(intData, noOfRowsToPad)

        return dupList
    
    
    def load_integers_from_seclist(self) -> list:
        
        #filePath = self.sm.get_file_names_of_directory()
        content = self.sm.download_file_as_str('digit/numeric-fields-only.txt')
        decoded = content.decode('utf-8')
        splitted = decoded.split("\n")                  
        return splitted
    
    
    def load_superlarge_integer_from_seclist(self):
        
        #filePath = self.sm.get_file_names_of_directory()
        content = self.sm.download_file_as_str('digit/pi-large.txt')
        decoded = content.decode('utf-8')
        return decoded
    
    