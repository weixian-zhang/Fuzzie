
import os
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

class StorageManager:
    
    def __init__(self, baseStorageUrl = 'https://strgfuzzie.blob.core.windows.net', fuzzDataContainer = 'fuzzdata') -> None:
        baseStorageUrl = baseStorageUrl
        fuzzDataContainer = fuzzDataContainer
        
        
    def download_file_as_str(self, fileName, directory = '') -> str:
        
       if directory != '':
            fileName = os.path.join(directory, fileName)
            
       blobClient = BlobClient(account_url=self.baseStorageUrl, container_name=self.fuzzDataContainer, blob_name=fileName)
       
       data = str(blobClient.download_blob().readall())
       
       return data
       
       