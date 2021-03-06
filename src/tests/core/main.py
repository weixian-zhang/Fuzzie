import os, sys
from pathlib import Path
import pandas as pd

projPath = Path(__file__).parent.parent.parent # /src
corePath = os.path.join(projPath, 'core')
sys.path.append(corePath)
datafactoryPath = os.path.join(corePath, 'datafactory')
sys.path.append(datafactoryPath)

currentFolder = Path(__file__).parent

from openapi3_apicontext_init_manager import OpenApi3ApiInitManager
from data_factory import DataFactory

def test_openapi3_initer():
    
    apiFilePath = os.path.join(currentFolder, 'apis.yaml')
    
    apiIniter = OpenApi3ApiInitManager()
    
    apiIniter.load_openapi3_file(apiFilePath)
    
    
def test_data_factory():
    
    dataf = DataFactory()
    
    df = dataf.generate_fuzz_dataset()
    
    

if __name__ == '__main__':
    # test_openapi3_initer()
    test_data_factory()