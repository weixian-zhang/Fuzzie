import unittest
from pathlib import Path
import os, sys
from eventstore import EventStore

projectDirPath = os.path.dirname(Path(__file__))
hostname = 'http://localhost'
port = 5000

sys.path.insert(0, os.path.join(projectDirPath, 'api_discovery'))

from fuzzmanager import FuzzManager

class TestFuzzManager(unittest.TestCase):
    
    
    def test_openapi3_get_params_path_object_yaml(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-get-params-path-object.yaml') 
        
        fm = FuzzManager(EventStore())
    
        fm.set_fuzzExecConfig(hostname=hostname, port=port, isAnonymous=True)
        
        fm.create_fuzz_context_from_openapi3_spec_file(openapi3Yaml)
        


if __name__ == '__main__':
    unittest.main()