import os
from azure.storage.blob import BlobPrefix, BlockBlobService
from numpy import append

class StorageManager:
    
    def __init__(self, 
                 baseStorageUrl = 'https://strgfuzzie.blob.core.windows.net/fuzzdata?st=2022-07-21T14:24:08Z&se=2026-07-21T22:24:08Z&si=vscode-ext-readonly&spr=https&sv=2021-06-08&sr=c&sig=%2FGX0GIfi5BlJ3jazJRPDpwYT%2BOgmEAElfbUV9RGTpr8%3D', 
                 fuzzDataContainer = 'fuzzdata') -> None:
        self.accountName = 'strgfuzzie'
        self.sastoken = 'st=2022-07-21T14:26:38Z&se=2026-07-21T22:26:38Z&si=vscode-ext-readonly&spr=https&sv=2021-06-08&sr=c&sig=udVzijpNVJVNpm3B%2Bzj%2B5R%2FqMfNaElp%2FsjBC4nfy82I%3D'
        self.baseStorageUrl = baseStorageUrl
        self.fuzzDataContainer = fuzzDataContainer
        
        
    def download_file_as_str(self, blobNamePath) -> str:
              
       bbsvc = BlockBlobService(account_name=self.accountName, sas_token=self.sastoken)
        
       blob = bbsvc.get_blob_to_text(self.fuzzDataContainer, blobNamePath)
              
       return blob.content
   
   
    def get_file_names_of_directory(self, startDir) -> list:
        
      try:
          
       bbsvc = BlockBlobService(account_name=self.accountName, sas_token=self.sastoken)
       
       blobNames = bbsvc.list_blob_names(self.fuzzDataContainer, prefix=startDir)
       
       return blobNames.items
           
      except Exception as e:
          #TODO: logging
          print(e)        
   
    def get_last_modified_datetime(self):
        pass