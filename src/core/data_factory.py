
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
       
       def generate_naughty_string(self):
           pass
       
       def generate_naughty_char(self):
           pass
       
       def generate_naughty_integer(self):
           pass
       
       def generate_naughty_files(self):
           pass
       
       def generate_date_of_diff_formats(self):
           pass