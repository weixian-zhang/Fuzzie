
import os
from azure.storage.blob import BlobClient

class StorageManager:
    
    def __init__(self, baseStorageUrl = 'https://strgfuzzie.blob.core.windows.net', fuzzDataContainer = 'fuzzdata') -> None:
        self.baseStorageUrl = baseStorageUrl
        self.fuzzDataContainer = fuzzDataContainer
        
        
    def download_file_as_str(self, fileName, directory = '') -> str:
        
       if directory != '':
            fileName = os.path.join(directory, fileName)
            
       blobClient = BlobClient(account_url=self.baseStorageUrl, container_name=self.fuzzDataContainer, blob_name=fileName)
       
       data = str(blobClient.download_blob().readall())
       
       return data
       
       
class DataFactory:
    
    def __init__(self) -> None:
        self.localDataDirectory = './' # directory location differs from clients. For e.g: vscode = vscode.workspace.workspaceFolders[0].uri.path
        self.fuzzdataDirectoryName = 'fuzzdata'
        self.dataRows = 10000 
    
    def generate_fuzz_dataset(self):
        pass
    
    def generate_naughty_string(self):
        pass
    
    def generate_char(self):
        pass
    
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