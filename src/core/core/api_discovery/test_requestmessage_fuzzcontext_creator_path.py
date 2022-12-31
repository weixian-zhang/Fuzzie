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

class TestRequestMessageFuzzContextCreator_By_Path(unittest.TestCase):
    
    def test_reqmsg_parser_get_path_without_path(self):
    
        rq = '''
           GET https://example.com HTTP/1.1
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
        
        # self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        # self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '')
        # self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '')
    
    def test_reqmsg_parser_get_path(self):

        rq = '''
           GET https://example.com/comments/{{digit}} HTTP/1.1
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
        
        # self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        # self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '')
        # self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/comments/{{digit}}')
        
    def test_reqmsg_parser_get_path_2(self):
    
        rq = '''
           GET https://example.com/comments/{{digit}}/second_comment/{{digit}}/third_comment/{{digit}} HTTP/1.1
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
        
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/comments/{{digit}}/second_comment/{{digit}}/third_comment/{{digit}}')
        
    def test_reqmsg_parser_get_path_with_querystring(self):
        
        rq = '''
           GET https://example.com/comments/{{digit}}/second_comment/{{digit}}/third_comment/{{digit}}?name={{name}}&age={{digit}} HTTP/1.1
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
        
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{name}}&age={{digit}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{name}}&age={{digit}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/comments/{{digit}}/second_comment/{{digit}}/third_comment/{{digit}}')
        
    def test_reqmsg_parser_get_path_only(self):
        
        rq = '''
           https://example.com/comments/{{digit}}/second_comment/{{digit}}/third_comment/{{digit}}/name/{{string}}
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
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/comments/{{digit}}/second_comment/{{digit}}/third_comment/{{digit}}/name/{{string}}')
        
        
    def test_reqmsg_parser_get_verb_and_path(self):
        
        rq = '''
           PUT https://example.com/comments/{{digit}}/second_comment/{{digit}}/third_comment/{{digit}}/name/{{string}}
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
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/comments/{{digit}}/second_comment/{{digit}}/third_comment/{{digit}}/name/{{string}}')
        
if __name__ == '__main__':
    unittest.main()