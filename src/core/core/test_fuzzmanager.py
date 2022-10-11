
import os, sys
from pathlib import Path
projectDirPath = os.path.dirname(Path(__file__))
sys.path.insert(0, os.path.join(projectDirPath, 'api_discovery'))

from eventstore import EventStore
import unittest
from servicemanager import ServiceManager

hostname = 'http://localhost'
port = 5000




class TestFuzzManager(unittest.TestCase):
    
    
    def test_openapi3_GET_path_object(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-get-params-path-object.yaml') 
        
        fm = ServiceManager(EventStore())
    
        fm.new_fuzzcontext(hostname=hostname, port=port, isAnonymous=True)
        
        fuzzcontext = fm.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        
    def test_openapi3_POST_multipartform(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-post_multipart-form-data.yaml') 
        
        fm = ServiceManager(EventStore())
    
        fm.new_fuzzcontext(hostname=hostname, port=port, isAnonymous=True)
        
        fuzzcontext = fm.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].bodyDataTemplate), 0)
        
    
    def test_openapi3_GET_headers_cookies_params(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-GET-headers-cookies-params.yaml') 
        
        fm = ServiceManager(EventStore())
    
        fm.new_fuzzcontext(hostname=hostname, port=port, isAnonymous=True)
        
        fuzzcontext = fm.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].headerDataTemplate), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].cookieDataTemplate), 0)
        


if __name__ == '__main__':
    unittest.main()