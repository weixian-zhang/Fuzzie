
from naughty_string_generator import NaughtyStringGenerator
import pandas as pd

class FileData:
    fileName = ''
    content = ''
       
       
class DataFactory:
    
    def __init__(self) -> None:

        self.df = pd.DataFrame()
        self.localDataDirectory = './' # directory location differs from clients. For e.g: vscode = vscode.workspace.workspaceFolders[0].uri.path
        self.fuzzdataDirectoryName = 'fuzzdata'
        self.dataRows = 10000 
    
    def generate_fuzz_dataset(self) -> pd.DataFrame:
        df = self.generate_naughty_string()
        return df
    
    def generate_naughty_string(self):
        
        sg = NaughtyStringGenerator()
        
        ns = sg.get_naughty_strings()
        
        self.df['naughtstrings'] = ns
    
    def generate_char(self):
        pass
    
    def generate_bool(self):
        bools = [True, False, None, 0, 1, 'true', 'false', 'yes', 'no', '1', '0', 't', 'f', 'T', 'F', 'TRUE', 'FALSE']
        return bools
    
    def generate_integer(self):
        pass
    
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