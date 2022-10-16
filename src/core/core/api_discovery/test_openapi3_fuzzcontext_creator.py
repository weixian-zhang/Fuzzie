
import os
from pathlib import Path
projectDirPath = os.path.dirname(Path(__file__))
# sys.path.insert(0, os.path.join(projectDirPath, 'api_discovery'))

from openapi3_discoverer import OpenApi3ApiDiscover
from openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.fuzzcontext import FuzzMode
from eventstore import EventStore
import unittest

hostname = 'http://localhost'
port = 5000

class TestFuzzManager(unittest.TestCase):
    
    
    def test_openapi3_GET_path_object(self):
        
        filePath = 'testdata\\testdata-openapi3-get-params-path-object.yaml'
        openapi3Yaml = os.path.join(projectDirPath, filePath)
        
        openapi3Dis = OpenApi3ApiDiscover()
        apicontext = openapi3Dis.load_openapi3_file(openapi3Yaml)
        
        fcc = OpenApi3FuzzContextCreator()
        fcc.new_fuzzcontext(
                            hostname=hostname,
                            port=port,
                            fuzzMode= 'Quick',
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicUsername='',
                            basicPassword='',
                            bearerTokenHeader='',
                            bearerToken='',
                            apikeyHeader='',
                            apikey='',
                            filePath=filePath)
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        self.assertEqual(len(fuzzcontext.fuzzcaseSets), 1)
        
        self.assertGreaterEqual(len(fuzzcontext.fuzzcaseSets[0].pathDataTemplate), 0)
        
        
    def test_openapi3_POST_multipartform(self):
        
        openapi3Yaml = os.path.join(projectDirPath, 'testdata\\testdata-openapi3-post_multipart-form-data.yaml') 
        
        openapi3Dis = OpenApi3ApiDiscover()
        apicontext = openapi3Dis.load_openapi3_file(openapi3Yaml)
        
        fcc = OpenApi3FuzzContextCreator()
        fcc.new_fuzzcontext(hostname=hostname,
                            port=port,
                            fuzzMode= 'Quick',
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicUsername='',
                            basicPassword='',
                            bearerTokenHeader='',
                            bearerToken='',
                            apikeyHeader='',
                            apikey='',
                            filePath='testdata\\testdata-openapi3-post_multipart-form-data.yaml')
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].bodyDataTemplate), 0)
        
    
    def test_openapi3_by_Url_1(self):
        
        url = 'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/link-example.yaml'
        
        openapi3Dis = OpenApi3ApiDiscover()
        apicontext = openapi3Dis.load_openapi3_url(url)
        
        fcc = OpenApi3FuzzContextCreator()
        fcc.new_fuzzcontext(hostname=hostname,
                            port=port,
                            fuzzMode= 'Quick',
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicUsername='',
                            basicPassword='',
                            bearerTokenHeader='',
                            bearerToken='',
                            apikeyHeader='',
                            apikey='',
                            url=url)
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        self.assertEqual(len(fuzzcontext.fuzzcaseSets), 6)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[5].pathDataTemplate), 0)
        
    
    def test_openapi3_GET_headers_cookies_params(self):
        
        filePath = 'testdata\\testdata-openapi3-GET-headers-cookies-params.yaml'
        openapi3Yaml = os.path.join(projectDirPath, filePath) 
        
        openapi3Dis = OpenApi3ApiDiscover()
        apicontext = openapi3Dis.load_openapi3_file(openapi3Yaml)
        
        fcc = OpenApi3FuzzContextCreator()
        fcc.new_fuzzcontext(hostname=hostname,
                            port=port,
                            fuzzMode= 'Quick',
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicUsername='',
                            basicPassword='',
                            bearerTokenHeader='',
                            bearerToken='',
                            apikeyHeader='',
                            apikey='',
                            filePath=filePath)
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].headerDataTemplate), 0)
        
        self.assertGreater(len(fuzzcontext.fuzzcaseSets[0].cookieDataTemplate), 0)
        


if __name__ == '__main__':
    unittest.main()