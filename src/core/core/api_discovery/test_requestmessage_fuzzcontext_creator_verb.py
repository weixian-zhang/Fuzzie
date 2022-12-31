import unittest
import base64
import os
import sys
from pathlib import Path

projectDirPath = os.path.dirname(Path(__file__))
parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)

sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from models.webapi_fuzzcontext import SupportedAuthnType

from webapi_fuzzcontext import ApiFuzzCaseSet, ApiFuzzContext
from requestmessage_fuzzcontext_creator import RequestMessageFuzzContextCreator

class TestRequestMessageFuzzContextCreator(unittest.TestCase):
    
    
    def test_reqmsg_parser_without_get(self):

        rq = '''
           https://example.com/comments/1 HTTP/1.1
        '''
        
        rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rqB64
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == 'https://example.com/comments/1')
        
    def test_reqmsg_parser_with_get(self):
    
        rq = '''
           GET https://example.com/comments/1 HTTP/1.1
        '''
        
        rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rqB64
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == 'https://example.com/comments/1')
        
    def test_reqmsg_parser_with_post(self):
    
        rq = '''
           POST https://example.com/comments/1 HTTP/1.1
        '''
        
        rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rqB64
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == 'https://example.com/comments/1')
        
    
    def test_reqmsg_parser_with_put(self):
        
        rq = '''
           PUT https://example.com/comments/1 HTTP/1.1
        '''
        
        rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rqB64
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'PUT')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == 'https://example.com/comments/1')
        
    def test_reqmsg_parser_with_delete(self):
        
        rq = '''
           DELETE https://example.com/comments/1 HTTP/1.1
        '''
        
        rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rqB64
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'DELETE')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == 'https://example.com/comments/1')

if __name__ == '__main__':
    unittest.main()