
from naughty_string_generator import NaughtyStringGenerator
from integer_generator import IntegerGenerator
import pandas as pd

class FileData:
    fileName = ''
    content = ''

class FileData:
    name = ''
    content = ''

#Fuzzie uses Seclist(https://github.com/danielmiessler/SecLists) and in addition generate its own data 
class DataFactory:
    
    def __init__(self) -> None:

        # file column is of type FileData
        self.df = pd.DataFrame({
            'naughtystring': [],
            'integer': [],
            'float': [],
            'datetime': [],
            'chars': [],
            'file': []
        })
        
        self.localDataDirectory = './' # directory location differs from clients. For e.g: vscode = vscode.workspace.workspaceFolders[0].uri.path
        self.fuzzdataDirectoryName = 'fuzzdata'
        self.dataRows = 10000 
    
    def generate_fuzz_dataset(self) -> pd.DataFrame:
        
        nsdf = self.generate_naughty_string()
        self.df['naughtystring'] = nsdf
        
        nsLength = len(nsdf)
        
        # generate and pad integer data to be equal rows to naughty-strings 
        intdf = self.generate_integer(nsLength)
        self.df['integer'] = intdf
        
        # debugging only
        for index, row in self.df.iterrows():
            print(row['naughtystring'], row['integer'])
        
        return self.df
    
    def generate_naughty_string(self):
        
        sg = NaughtyStringGenerator()
        
        df = sg.generate_naughty_strings()
        
        return df
        
    def generate_integer(self, noOfRowsToPad) -> list:
        
        ig = IntegerGenerator()
        intdf = ig.generate_integers(noOfRowsToPad)
        return intdf
    
    def generate_char(self):
        pass
    
    def generate_bool(self):
        bools = [True, False, None, 0, 1, 'true', 'false', 'yes', 'no', '1', '0', 't', 'f', 'T', 'F', 'TRUE', 'FALSE']
        return bools
    
    
    def generate_float(self):
        pass
    
    def generate_naughty_files(self):
        pass
    
    def generate_date_of_diff_formats(self):
        #generate all valid date formats
        # https://docs.oracle.com/cd/E41183_01/DR/Date_Format_Types.html
        
        #generate invalid date formats
        
        #input naughty strings
        pass