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

class TestRequestMessageFuzzContextCreator_By_Body(unittest.TestCase):
    
    # def test_reqmsg_parser_body_xwwwformurlencoded_1(self):
    
    #     rq = '''
    #        POST https://example.com/user?name={{username}}&address={{string}}
    #        Content-Type: 

    #        name={{username}}
    #        &password={{password}}
    #     '''
        
    #     rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rqB64
    #                         )
        
    #     self.assertTrue(ok)
    #     self.assertTrue(error == '')
    #     self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '')

    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == 'name={{username}}&password={{password}}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == 'name={{username}}&password={{password}}')
        
    
    # def test_reqmsg_parser_body_without_breakline_marker(self):
        
    #     rq = '''
    #        POST https://example.com/user?name={{username}}&address={{string}}
    #        name={{username}}
    #        &password={{password}}
    #     '''
        
    #     rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rqB64
    #                         )
        
    #     self.assertTrue(ok)
    #     self.assertTrue(error == '')
    #     self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '')

    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '')
        
        
    # def test_reqmsg_parser_body_without_breakline_marker(self):
        
    #     rq = '''
    #        POST https://example.com/user?name={{username}}&address={{string}}
           
    #        name={{username}}
    #        &password={{password}}
    #     '''
        
    #     rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rqB64
    #                         )
        
    #     self.assertTrue(ok)
    #     self.assertTrue(error == '')
    #     self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '')

    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == 'name={{username}}&password={{password}}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == 'name={{username}}&password={{password}}')
        
    
    def test_reqmsg_parser_body_json(self):
        
        import re
        
        
        

        
        rq = '''
           POST https://example.com/user?name={{username}}&address={{string}}
           Authorization: {{ string }}
           CustomHeader-1: {{ digit }}
           CustomHeader-2: {{ filename }}
           CustomHeader-3: {{ username }}
           Content-Type: application/json
           
           {
                "name": {{ username }},
                "time": {{ datetime }}
           }
           
           
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
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
        self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{ "Authorization": " {{ string }}", "CustomHeader-1": " {{ digit }}", "CustomHeader-2": " {{ filename }}", "CustomHeader-3": " {{ username }}", "Content-Type": " application/json"}')
        self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{ "Authorization": " {{ string }}", "CustomHeader-1": " {{ digit }}", "CustomHeader-2": " {{ filename }}", "CustomHeader-3": " {{ username }}", "Content-Type": " application/json"}')

        # self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == 'name={{username}}&password={{password}}')
        # self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == 'name={{username}}&password={{password}}')
    
        
        
if __name__ == '__main__':
    unittest.main()