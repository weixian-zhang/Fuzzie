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

class TestRequestMessageFuzzContextCreator_By_QueryString(unittest.TestCase):
    
    def test_reqmsg_parser_with_qs_without_path(self):
    
        rq = '''
           https://example.com?name={{username}}&address={{string}}
        '''
    
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rq
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{ eval(\'username\') }}&address={{ eval(\'string\') }}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '')
        
        
    def test_reqmsg_parser_qs_with_newline_1(self):
        
        rq = '''
           https://example.com/user
           ?name={{username}}
           &address={{string}}
        '''
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rq
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{ eval(\'username\') }}&address={{ eval(\'string\') }}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        
    def test_reqmsg_parser_qs_with_newline_2(self):
        
        rq = '''
           https://example.com/user?name={{username}}
            &address={{string}}
        '''
    
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rq
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{ eval(\'username\') }}&address={{ eval(\'string\') }}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        
    def test_reqmsg_parser_qs_with_newline_3(self):
        
        rq = '''
           https://example.com/user
            ?name={{username}}&address={{string}}
        '''
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rq
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == "?name={{ eval('username') }}&address={{ eval('string') }}")
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        
    def test_reqmsg_parser_qs_with_newline_4(self):
        
        rq = '''
           
           https://example.com/user HTTP/1.1
            ?name={{username}}
            &address={{string}}
            &order=5
            &mode={{string}}
           a: "b"
            
        '''
        
        rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
                            apiDiscoveryMethod= "request_message",
                            name= "request-message-test",
                            hostname='https://example.com',
                            port='443',
                            authnType=SupportedAuthnType.Anonymous.name,
                            fuzzcaseToExec=500,
                            openapi3FilePath='',
                            requestTextContent= rq
                            )
        
        self.assertTrue(ok)
        self.assertTrue(error == '')
        self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
        self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'GET')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}&order=5&mode={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{ eval(\'username\') }}&address={{ eval(\'string\') }}&order=5&mode={{ eval(\'string\') }}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        
        
if __name__ == '__main__':
    unittest.main()