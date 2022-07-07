import os, sys
from pathlib import Path
projPath = Path(__file__).parent.parent.parent # /src
corePath = os.path.join(projPath, 'core')
#projPath =str(projPath).replace('/', '\\')
#print(corePath)
sys.path.append(corePath)
#print(sys.path)


currentFolder = Path(__file__).parent

from api_init_manager import ApiInitManager

def test():
    
    apiFilePath = os.path.join(currentFolder, 'apis.yaml')
    
    apiIniter = ApiInitManager()
    
    apiIniter.load_openapi3_yaml_file(apiFilePath)

if __name__ == '__main__':
    test()