import os, sys
from pathlib import Path
import pandas as pd

projPath = Path(__file__).parent.parent.parent # /src
corePath = os.path.join(projPath, 'core')
sys.path.append(corePath)

initmanagerPath = os.path.join(corePath, 'api-initmanager')
sys.path.append(initmanagerPath)

corporafactoryPath = os.path.join(corePath, 'corporafactory')
sys.path.append(corporafactoryPath)

currentFolder = Path(__file__).parent

from openapi3_init_manager import OpenApi3ApiInitManager
from data_factory import corporafactory
from fuzzie_core import Fuzzie

def test_openapi3_file_initer():
    
    apiFilePath = os.path.join(currentFolder, 'apis.yaml') #'sample-linode-openapi.yaml')
    
    apiIniter = OpenApi3ApiInitManager()
    
    apiIniter.load_openapi3_file(apiFilePath)
    
def test_openapi3_url_initer():
    
    url = 'http://localhost:5000/swagger/yaml'
    
    apiIniter = OpenApi3ApiInitManager()
    
    apiIniter.load_openapi3_url(url)
    
    
def test_data_factory():
    
    dataf = corporafactory()
    
    df = dataf.generate_fuzz_dataset()
    
    

if __name__ == '__main__':
    # test_openapi3_initer()
    # test_data_factory()
    #test_openapi3_url_initer()
    test_openapi3_file_initer()