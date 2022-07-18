import os
from azure.storage.blob import BlobClient

class StorageManager:
    
    def __init__(self, baseStorageUrl = 'https://strgfuzzie.blob.core.windows.net', fuzzDataContainer = 'fuzzdata') -> None:
        self.baseStorageUrl = baseStorageUrl
        self.fuzzDataContainer = fuzzDataContainer
        
        
    def download_file_as_str(self, fileName, *directories) -> str:
        
       dir = os.path.join(*directories)
       fileName =  os.path.join(dir, fileName)
            
       blobClient = BlobClient(account_url=self.baseStorageUrl, container_name=self.fuzzDataContainer, blob_name=fileName)
       
       binaryData = blobClient.download_blob().readall()
       
       return binaryData