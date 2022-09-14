from storagemanager import StorageManager
import pandas as pd

# integer data requirements
# Seclist already contains various positive/negative integer data and a large 4MB interger
# self generate 
    # prepend 0s
# repeat data base on number of records in naughty_strings
class NumericGenerator:
    
    def __init__(self):
        
        self.sm = StorageManager()
        self.specialData = [0.1000000000000000055511151231257827021181583404541015625]
        
        self.piLargerIntegerFileName = 'digit/pi-large.txt'
        
        self.numeric_fieldsFileName = 'digit/numeric-fields-only.txt'
    
    def generate_numeric_values(self, noOfRowsToPad = 1000) -> pd.DataFrame:
        
        df = pd.DataFrame()
        
        numericDF = self.load_numerics_from_seclist(df)
        
        largePIIDF = self.load_superlarge_integer_from_seclist(df)
        
        mergedDF = pd.DataFrame()
        
        mergedDF = pd.concat([mergedDF, numericDF, largePIIDF])
        
        
        
        return mergedDF
    
    def load_numerics_from_seclist(self, df: pd.DataFrame):
        
        #filePath = self.sm.get_file_names_of_directory()
        content = self.sm.download_file_as_str(self.numeric_fieldsFileName)
        decoded = content.decode('utf-8')
        
        splitted = decoded.split('\n')
        
        for s in splitted:
            df = df.append({"content": s}, ignore_index=True)
            
        return df
    
    def load_superlarge_integer_from_seclist(self, df: pd.DataFram):
        
        #filePath = self.sm.get_file_names_of_directory()
        content = self.sm.download_file_as_str(self.piLargerIntegerFileName)
        decoded = content.decode('utf-8')
        splitted = decoded.split('\n')
        
        for s in splitted:
            df = df.append({"content": s}, ignore_index=True)
            
        return df
    
    