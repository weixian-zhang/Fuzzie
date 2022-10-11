import unittest
from pathlib import Path
import os, sys, json
from eventstore import EventStore

projectDirPath = os.path.dirname(Path(__file__))
hostname = 'http://localhost'
port = 5000

sys.path.insert(0, os.path.join(projectDirPath, 'api_discovery'))

from fuzzmanager import FuzzManager

class TestFuzzManager(unittest.TestCase):
    
    
    def test_openapi3_GET_path_object(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-get-params-path-object.yaml') 
        
        fm = FuzzManager(EventStore())
    
        fm.set_fuzzExecConfig(hostname=hostname, port=port, isAnonymous=True)
        
        fuzzcontext = fm.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        
    def test_openapi3_POST_multipartform(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-post_multipart-form-data.yaml') 
        
        fm = FuzzManager(EventStore())
    
        fm.set_fuzzExecConfig(hostname=hostname, port=port, isAnonymous=True)
        
        fuzzcontext = fm.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].bodyDataTemplate), 0)
        
    
    def test_openapi3_GET_headers_cookies_params(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-GET-headers-cookies-params.yaml') 
        
        fm = FuzzManager(EventStore())
    
        fm.set_fuzzExecConfig(hostname=hostname, port=port, isAnonymous=True)
        
        fuzzcontext = fm.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].headerDataTemplate), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].cookieDataTemplate), 0)
        


if __name__ == '__main__':
    unittest.main()