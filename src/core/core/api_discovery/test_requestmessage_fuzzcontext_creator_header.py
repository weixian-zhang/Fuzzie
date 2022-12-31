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

class TestRequestMessageFuzzContextCreator_By_Header(unittest.TestCase):
    
    def test_reqmsg_parser_headers_with_singleline_qs_1(self):
    
        rq = '''
           https://example.com/user?name={{username}}&address={{string}}
           Content-Type: application/xml
           Authorization: {{string}}
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
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": " application/xml", "Authorization": " {{string}}"}')
        self.assertTrue(len(apicontext.fuzzcaseSets[0].headerDataTemplate) == 2)
        
        
    def test_reqmsg_parser_headers_with_singleline_qs_2(self):
        
        rq = '''
           https://example.com/user?name={{username}}&address={{string}}
           Content-Type: application/xml
           Authorization: {{ string }}
           CustomHeader-1: {{ digit }}
           CustomHeader-2: {{ filename }}
           CustomHeader-3: {{ username }}
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
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": " application/xml", "Authorization": " {{ string }}", "CustomHeader-1": " {{ digit }}", "CustomHeader-2": " {{ filename }}", "CustomHeader-3": " {{ username }}"}')
        self.assertTrue(len(apicontext.fuzzcaseSets[0].headerDataTemplate) == 5)
        
        
    def test_reqmsg_parser_headers_with_multiline_qs_1(self):
        
        rq = '''
           https://example.com/user
                ?name={{username}}&address={{string}}
                
           Content-Type: application/xml
           Authorization: {{ string }}
           CustomHeader-1: {{ digit }}
           CustomHeader-2: {{ filename }}
           CustomHeader-3: {{ username }}
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
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{username}}&address={{string}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": " application/xml", "Authorization": " {{ string }}", "CustomHeader-1": " {{ digit }}", "CustomHeader-2": " {{ filename }}", "CustomHeader-3": " {{ username }}"}')
        self.assertTrue(len(apicontext.fuzzcaseSets[0].headerDataTemplate) == 5)
        
    
    def test_reqmsg_parser_headers_with_multiline_qs_1(self):
        
        rq = '''
           https://example.com/user
                ?name={{username}}
                &address={{string}}
                &mode={{string}}
                &geek={{bool}}
                
           Content-Type: application/xml
           Authorization: {{ string }}
           CustomHeader-1: {{ digit }}
           CustomHeader-2: {{ filename }}
           CustomHeader-3: {{ username }}
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
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}&mode={{string}}&geek={{bool}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{username}}&address={{string}}&mode={{string}}&geek={{bool}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": " application/xml", "Authorization": " {{ string }}", "CustomHeader-1": " {{ digit }}", "CustomHeader-2": " {{ filename }}", "CustomHeader-3": " {{ username }}"}')
        self.assertTrue(len(apicontext.fuzzcaseSets[0].headerDataTemplate) == 5)
        
    
    def test_reqmsg_parser_headers_with_multiline_qs_invalid_header_1(self):
        
        rq = '''
           https://example.com/user
                ?name={{username}}
                &address={{string}}
                &mode={{string}}
                &geek={{bool}}
                
           Content-Type: application/xml
           Authorization: 
           CustomHeader-1: {{ digit }}
           CustomHeader-2 {{ filename }}
           CustomHeader-3: {{ username }}
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
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}&mode={{string}}&geek={{bool}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{username}}&address={{string}}&mode={{string}}&geek={{bool}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": " application/xml", "CustomHeader-1": " {{ digit }}", "CustomHeader-3": " {{ username }}"}')
        self.assertTrue(len(apicontext.fuzzcaseSets[0].headerDataTemplate) == 3)
        
        
    def test_reqmsg_parser_headers_with_multiline_qs_invalid_header_1(self):
        
        rq = '''
           https://example.com/user
                ?name={{username}}
                &address={{string}}
                &mode={{string}}
                &geek={{bool}}
                
           Content-Type: application/xml
           Authorization: 
           CustomHeader-1: {{ digit }}
           CustomHeader-2 {{ filename }}
           : {{ username }}
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
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{username}}&address={{string}}&mode={{string}}&geek={{bool}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{username}}&address={{string}}&mode={{string}}&geek={{bool}}')
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": " application/xml", "CustomHeader-1": " {{ digit }}"}')
        self.assertTrue(len(apicontext.fuzzcaseSets[0].headerDataTemplate) == 2)
        
        
        
if __name__ == '__main__':
    unittest.main()