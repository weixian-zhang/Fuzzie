import os, sys
from pathlib import Path
projPath = Path(__file__).parent.parent.parent # /src
corePath = os.path.join(projPath, 'core')
#projPath =str(projPath).replace('/', '\\')
#print(corePath)
sys.path.append(corePath)
#print(sys.path)


currentFolder = Path(__file__).parent

from openapi3_apicontext_init_manager import OpenApi3ApiInitManager
from data_factory import StorageManager

def test_openapi3_initer():
    
    apiFilePath = os.path.join(currentFolder, 'apis.yaml')
    
    apiIniter = OpenApi3ApiInitManager()
    
    apiIniter.load_openapi3_file(apiFilePath)
    
    
def test_storagemanager():
    
    sm = StorageManager()
    
    sm.download_file_as_str('blns.json', 'naughty-strings')
    
    

if __name__ == '__main__':
    # test_openapi3_initer()
    test_storagemanager()