
import os, sys
from pathlib import Path
projectDirPath = os.path.dirname(Path(__file__))
sys.path.insert(0, os.path.join(projectDirPath, 'api_discovery'))

from openapi3_fuzzcontext_creator import FuzzContextCreator
from models.fuzzcontext import ApiFuzzContext, FuzzMode
from eventstore import EventStore
import unittest

hostname = 'http://localhost'
port = 5000




class TestFuzzManager(unittest.TestCase):
    
    
    def test_openapi3_GET_path_object(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-get-params-path-object.yaml') 
        
        fcc = FuzzContextCreator()
        fcc.new_fuzzcontext(hostname=hostname,
                            port=port,
                            fuzzMode= FuzzMode.Quick,
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicAuthnUserName='',
                            basicAuthnPassword='',
                            bearerTokenHeaderName='',
                            bearerToken='',
                            apikeyAuthnHeaderName='',
                            apikeyAuthnKey='')
        
        fuzzcontext = fcc.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        
    def test_openapi3_POST_multipartform(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-post_multipart-form-data.yaml') 
        
        fcc = FuzzContextCreator()
        fcc.new_fuzzcontext(hostname=hostname,
                            port=port,
                            fuzzMode= FuzzMode.Quick,
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicAuthnUserName='',
                            basicAuthnPassword='',
                            bearerTokenHeaderName='',
                            bearerToken='',
                            apikeyAuthnHeaderName='',
                            apikeyAuthnKey='')
        
        fuzzcontext = fcc.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].bodyDataTemplate), 0)
        
    
    def test_openapi3_GET_headers_cookies_params(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'api_discovery\\testdata\\testdata-openapi3-GET-headers-cookies-params.yaml') 
        
        fcc = FuzzContextCreator()
        fcc.new_fuzzcontext(hostname=hostname,
                            port=port,
                            fuzzMode= FuzzMode.Quick,
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicAuthnUserName='',
                            basicAuthnPassword='',
                            bearerTokenHeaderName='',
                            bearerToken='',
                            apikeyAuthnHeaderName='',
                            apikeyAuthnKey='')
        
        fuzzcontext = fcc.create_fuzzcontext_from_openapi3_spec_file(openapi3Yaml)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].headerDataTemplate), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].cookieDataTemplate), 0)
        


if __name__ == '__main__':
    unittest.main()