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

def test():
    
    apiFilePath = os.path.join(currentFolder, 'apis.yaml')
    
    apiIniter = OpenApi3ApiInitManager()
    
    apiIniter.load_openapi3_file(apiFilePath)

if __name__ == '__main__':
    test()