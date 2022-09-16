
# class FileData:
#     fileName = ''
#     content = ''

# class FileData:
#     name = ''
#     content = ''

# #Fuzzie uses Seclist(https://github.com/danielmiessler/SecLists) and in addition generate its own data 
# class DataFactory:
    
#     def __init__(self) -> None:
        
#         pass
    
    
    
    
    
    

#     #     # file column is of type FileData
#     #     self.df = pd.DataFrame({
#     #         'naughtystring': [],
#     #         'integer': [],
#     #         'float': [],
#     #         'datetime': [],
#     #         'chars': [],
#     #         'file': []
#     #     })
        
#     #     self.localDataDirectory = './' # directory location differs from clients. For e.g: vscode = vscode.workspace.workspaceFolders[0].uri.path
#     #     self.fuzzdataDirectoryName = 'fuzzdata'
#     #     self.dataRows = 10000 
    
#     # def generate_fuzz_dataset(self) -> pd.DataFrame:
        
#     #     ns = self.generate_naughty_string()
#     #     self.df['naughtystring'] = ns
        
#     #     rowsToPadAgainstNaughtyStrings = 15273 #len(nsdf)
        
#     #     # generate and pad integer data to be equal rows to naughty-strings 
#     #     ints = self.generate_integer(rowsToPadAgainstNaughtyStrings)
#     #     self.df['integer'] = ints
        
#     #     floats = self.generate_float(rowsToPadAgainstNaughtyStrings)
#     #     self.df['float'] = floats
        
#     #     # debugging only
#     #     # for index, row in self.df.iterrows():
#     #     #     print(f" strings: {row['naughtystring']}, ints: {row['integer']}, floats: {row['float']}")
        
#     #     return self.df
    
#     # def generate_naughty_string(self):
        
#     #     sg = NaughtyStringGenerator()
        
#     #     df = sg.generate_naughty_strings()
        
#     #     return df
        
#     # def generate_integer(self, noOfRowsToPad) -> list:
        
#     #     ig = IntegerGenerator()
#     #     ints = ig.generate_integers(noOfRowsToPad)
#     #     return ints
    
#     # def generate_char(self):
#     #     pass
    
#     # def generate_bool(self):
#     #     bools = [True, False, None, 0, 1, 'true', 'false', 'yes', 'no', '1', '0', 't', 'f', 'T', 'F', 'TRUE', 'FALSE']
#     #     return bools
    
    
#     # def generate_float(self, noOfRowsToPad):
#     #     fg = FloatGenerator()
#     #     floats = fg.generate_floats(noOfRowsToPad)
#     #     return floats
    
#     # def generate_naughty_files(self):
#     #     pass
    
#     # def generate_date_of_diff_formats(self):
#     #     #generate all valid date formats
#     #     # https://docs.oracle.com/cd/E41183_01/DR/Date_Format_Types.html
        
#     #     #generate invalid date formats
        
#     #     #input naughty strings
#     #     pass