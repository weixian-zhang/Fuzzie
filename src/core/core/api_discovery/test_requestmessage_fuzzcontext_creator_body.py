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
from utils import Utils
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
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rq
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
        
        
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rq
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
        
        
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rq
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
        
    
    # def test_reqmsg_parser_body_json(self):
        
          
    #     rq = '''
    #        POST https://example.com/user?name={{username}}&address={{string}}
    #        Authorization: {{ string }}
    #        CustomHeader-1: {{ digit }}
    #        CustomHeader-2: {{ filename }}
    #        CustomHeader-3: {{ username }}
    #        Content-Type: application/json
           
    #        {
    #             "name": {{ username }},
    #             "time": {{ datetime }}
    #        }
           
           
    #     '''
        
        
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rq
    #                         )
        
    #     self.assertTrue(ok)
    #     self.assertTrue(error == '')
    #     self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "application/json"}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "application/json"}')

    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '{"name": {{ username }},"time": {{ datetime }}}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '{"name": {{ username }},"time": {{ datetime }}}')
        
        
    # def test_reqmsg_parser_body_complex_json(self):
        
          
    #     rq = '''
    #        POST https://example.com/user?name={{username}}&address={{string}}
    #        Authorization: {{ string }}
    #        CustomHeader-1: {{ digit }}
    #        CustomHeader-2: {{ filename }}
    #        CustomHeader-3: {{ username }}
    #        Content-Type: application/json
           
    #        {
    #             "id": "0001",
    #             "type": "{{string}}",
    #             "name": "{{string}}",
    #             "ppu": {{digit}},
    #             "batters":
    #                 {
    #                     "batter":
    #                         [
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" }
    #                         ]
    #                 },
    #             "topping":
    #                 [
    #                     { "id": "5001", "name": "{{ my:[some],[dessert] }}" },
    #                     { "id": "5002", "name": "{{ my:[Glazed] }}" },
    #                     { "id": "5005", "name": "{{ my:[Sugar] }}" },
    #                 ]
    #         }
           
           
    #     '''
        
        
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rq
    #                         )
        
    #     self.assertTrue(ok)
    #     self.assertTrue(error == '')
    #     self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "application/json"}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "application/json"}')

    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
    
    
    # # invalid more than 1 breaklines between requestline and headers
    # # this will cause headers to be part of body
    # def test_reqmsg_parser_body_complex_json_multi_breakline(self):
        
          
    #     rq = '''
    #        POST https://example.com/user?name={{username}}&address={{string}}
           
           
           
           
           
           
           
           
    #        Authorization: {{ string }}
    #        CustomHeader-1: {{ digit }}
    #        CustomHeader-2: {{ filename }}
    #        CustomHeader-3: {{ username }}
    #        Content-Type: multipart/form-data
           
    #        {{ file   }}
           
    #        {
    #             "id": "0001",
    #             "type": "{{string}}",
    #             "name": "{{string}}",
    #             "ppu": {{digit}},
    #             "batters":
    #                 {
    #                     "batter":
    #                         [
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" }
    #                         ]
    #                 },
    #             "topping":
    #                 [
    #                     { "id": "5001", "name": "{{ my:[some],[dessert] }}" },
    #                     { "id": "5002", "name": "{{ my:[Glazed] }}" },
    #                     { "id": "5005", "name": "{{ my:[Sugar] }}" },
    #                 ]
    #         }
            
    #         {{ pdf   }}
           
    #     '''
        
        
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rqMsg
    #                         )
        
    #     self.assertTrue(ok)
    #     self.assertTrue(error == '')
    #     self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '')

    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == 'Authorization: {{ string }}CustomHeader-1: {{ digit }}CustomHeader-2: {{ filename }}CustomHeader-3: {{ username }}Content-Type: multipart/form-data{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == 'Authorization: {{ string }}CustomHeader-1: {{ digit }}CustomHeader-2: {{ filename }}CustomHeader-3: {{ username }}Content-Type: multipart/form-data{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
    
    #     self.assertTrue(len(apicontext.fuzzcaseSets[0].file) == 2)
        
        
    # def test_reqmsg_parser_body_multiple_files(self):
        
          
    #     rq = '''
    #        POST https://example.com/user?name={{username}}&address={{string}}
    #        Authorization: {{ string }}
    #        CustomHeader-1: {{ digit }}
    #        CustomHeader-2: {{ filename }}
    #        CustomHeader-3: {{ username }}
    #        Content-Type: multipart/form-data
           
    #        {{ file   }}
            
    #         {{ pdf   }}
            
    #         {{ image   }}
            
    #         {{ pdf   }}
           
    #     '''
        
        
        
    #     rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
        
        
    #     ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                         apiDiscoveryMethod= "request_message",
    #                         name= "request-message-test",
    #                         hostname='https://example.com',
    #                         port='443',
    #                         authnType=SupportedAuthnType.Anonymous.name,
    #                         fuzzcaseToExec=500,
    #                         openapi3FilePath='',
    #                         requestTextContent= rq
    #                         )
        
    #     self.assertTrue(ok)
    #     self.assertTrue(error == '')
    #     self.assertGreater(len(apicontext.fuzzcaseSets), 0)
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')
    
    #     self.assertTrue(len(apicontext.fuzzcaseSets[0].file) == 4)
        
        
    # # parsing body with
    # #     multiple files
    # #     json
    # #     multiple breaklines between header and body
    # def test_reqmsg_parser_body_multiple_files_complex_json(self):
            
          
    #         rq = '''
    #         POST https://example.com/user?name={{username}}&address={{string}}
    #         Authorization: {{ string }}
    #         CustomHeader-1: {{ digit }}
    #         CustomHeader-2: {{ filename }}
    #         CustomHeader-3: {{ username }}
    #         Content-Type: multipart/form-data
            
            
            
            
            
            
            
            
    #         {{ file   }}
                
    #             {{ pdf   }}
                
    #             {{ image   }}
                
                
    #             {
    #             "id": "0001",
    #             "type": "{{string}}",
    #             "name": "{{string}}",
    #             "ppu": {{digit}},
    #             "batters":
    #                 {
    #                     "batter":
    #                         [
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" }
    #                         ]
    #                 },
    #             "topping":
    #                 [
    #                     { "id": "5001", "name": "{{ my:[some],[dessert] }}" },
    #                     { "id": "5002", "name": "{{ my:[Glazed] }}" },
    #                     { "id": "5005", "name": "{{ my:[Sugar] }}" },
    #                 ]
    #         }
                
    #             {{ pdf   }}
            
    #         '''
            
            
            
    #         rqMsgFCCreator = RequestMessageFuzzContextCreator()
            
            
            
    #         ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                             apiDiscoveryMethod= "request_message",
    #                             name= "request-message-test",
    #                             hostname='https://example.com',
    #                             port='443',
    #                             authnType=SupportedAuthnType.Anonymous.name,
    #                             fuzzcaseToExec=500,
    #                             openapi3FilePath='',
    #                             requestTextContent= rq
    #                             )
            
    #         self.assertTrue(ok)
    #         self.assertTrue(error == '')
    #         self.assertGreater(len(apicontext.fuzzcaseSets), 0)
            
    #         self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
            
    #         self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')

    #         self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
        
    #         self.assertTrue(len(apicontext.fuzzcaseSets[0].file) == 4)
            
    # # parsing body with
    # #     no headers
    # #     multiple breaklines between requestline and body
    # #     multiple files
    # #     json 
    # #     multiple breaklines between header and body
    # def test_reqmsg_parser_body_no_header_breakline_multiple_files_complex_json(self):
            
          
    #         rq = '''
    #         POST https://example.com/user?name={{username}}&address={{string}}
            
            
            
            
            
            
            
            
    #         {{ file   }}
                
    #             {{ pdf   }}
                
    #             {{ image   }}
                
                
    #             {
    #             "id": "0001",
    #             "type": "{{string}}",
    #             "name": "{{string}}",
    #             "ppu": {{digit}},
    #             "batters":
    #                 {
    #                     "batter":
    #                         [
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" },
    #                             { "id": "{{digit}}", "type": "{{string}}" }
    #                         ]
    #                 },
    #             "topping":
    #                 [
    #                     { "id": "5001", "name": "{{ my:[some],[dessert] }}" },
    #                     { "id": "5002", "name": "{{ my:[Glazed] }}" },
    #                     { "id": "5005", "name": "{{ my:[Sugar] }}" },
    #                 ]
    #         }
                
    #             {{ pdf   }}
            
    #         '''
            
            
            
    #         rqMsgFCCreator = RequestMessageFuzzContextCreator()
            
            
            
    #         ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                             apiDiscoveryMethod= "request_message",
    #                             name= "request-message-test",
    #                             hostname='https://example.com',
    #                             port='443',
    #                             authnType=SupportedAuthnType.Anonymous.name,
    #                             fuzzcaseToExec=500,
    #                             openapi3FilePath='',
    #                             requestTextContent= rq
    #                             )
            
    #         self.assertTrue(ok)
    #         self.assertTrue(error == '')
    #         self.assertGreater(len(apicontext.fuzzcaseSets), 0)
            
    #         self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
            
    #         self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '')
    #         #self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')
    #         #self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')

    #         self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '{"id": "0001","type": "{{string}}","name": "{{string}}","ppu": {{digit}},"batters":{"batter":[{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" },{ "id": "{{digit}}", "type": "{{string}}" }]},"topping":[{ "id": "5001", "name": "{{ my:[some],[dessert] }}" },{ "id": "5002", "name": "{{ my:[Glazed] }}" },{ "id": "5005", "name": "{{ my:[Sugar] }}" },]}')
        
    #         self.assertTrue(len(apicontext.fuzzcaseSets[0].file) == 4)
            
            
    # # parsing body with
    # #     no headers
    # #     multiple files
    # #     xml 
    # #     multiple breaklines between header and body
    # def test_reqmsg_parser_body_no_header_breakline_multiple_files_complex_json(self):
            
          
    #         rq = '''
    #         POST https://example.com/user?name={{username}}&address={{string}}
    #         Content-Type: application/xml
            
    #         {{ file   }}
                
    #             {{ pdf   }}
                
    #             {{ image   }}
                
                
    #             <?xml version="1.0"?>
    #                 <catalog>
    #                 <book id="bk101">
    #                     <author>Gambardella, Matthew</author>
    #                     <title>XML Developer's Guide</title>
    #                     <genre>Computer</genre>
    #                     <price>44.95</price>
    #                     <publish_date>2000-10-01</publish_date>
    #                     <description>An in-depth look at creating applications 
    #                     with XML.</description>
    #                 </book>
    #                 <book id="bk102">
    #                     <author>Ralls, Kim</author>
    #                     <title>Midnight Rain</title>
    #                     <genre>Fantasy</genre>
    #                     <price>5.95</price>
    #                     <publish_date>2000-12-16</publish_date>
    #                     <description>A former architect battles corporate zombies, 
    #                     an evil sorceress, and her own childhood to become queen 
    #                     of the world.</description>
    #                 </book>
    #                 <book id="bk103">
    #                     <author>Corets, Eva</author>
    #                     <title>Maeve Ascendant</title>
    #                     <genre>Fantasy</genre>
    #                     <price>5.95</price>
    #                     <publish_date>2000-11-17</publish_date>
    #                     <description>After the collapse of a nanotechnology 
    #                     society in England, the young survivors lay the 
    #                     foundation for a new society.</description>
    #                 </book>
    #                 <book id="bk104">
    #                     <author>Corets, Eva</author>
    #                     <title>Oberon's Legacy</title>
    #                     <genre>Fantasy</genre>
    #                     <price>5.95</price>
    #                     <publish_date>2001-03-10</publish_date>
    #                     <description>In post-apocalypse England, the mysterious 
    #                     agent known only as Oberon helps to create a new life 
    #                     for the inhabitants of London. Sequel to Maeve 
    #                     Ascendant.</description>
    #                 </book>
    #                 <book id="bk105">
    #                     <author>Corets, Eva</author>
    #                     <title>The Sundered Grail</title>
    #                     <genre>Fantasy</genre>
    #                     <price>5.95</price>
    #                     <publish_date>2001-09-10</publish_date>
    #                     <description>The two daughters of Maeve, half-sisters, 
    #                     battle one another for control of England. Sequel to 
    #                     Oberon's Legacy.</description>
    #                 </book>
    #                 <book id="bk106">
    #                     <author>Randall, Cynthia</author>
    #                     <title>Lover Birds</title>
    #                     <genre>Romance</genre>
    #                     <price>4.95</price>
    #                     <publish_date>2000-09-02</publish_date>
    #                     <description>When Carla meets Paul at an ornithology 
    #                     conference, tempers fly as feathers get ruffled.</description>
    #                 </book>
    #                 <book id="bk107">
    #                     <author>Thurman, Paula</author>
    #                     <title>Splish Splash</title>
    #                     <genre>Romance</genre>
    #                     <price>4.95</price>
    #                     <publish_date>2000-11-02</publish_date>
    #                     <description>A deep sea diver finds true love twenty 
    #                     thousand leagues beneath the sea.</description>
    #                 </book>
    #                 <book id="bk108">
    #                     <author>Knorr, Stefan</author>
    #                     <title>Creepy Crawlies</title>
    #                     <genre>Horror</genre>
    #                     <price>4.95</price>
    #                     <publish_date>2000-12-06</publish_date>
    #                     <description>An anthology of horror stories about roaches,
    #                     centipedes, scorpions  and other insects.</description>
    #                 </book>
    #                 <book id="bk109">
    #                     <author>Kress, Peter</author>
    #                     <title>Paradox Lost</title>
    #                     <genre>Science Fiction</genre>
    #                     <price>6.95</price>
    #                     <publish_date>2000-11-02</publish_date>
    #                     <description>After an inadvertant trip through a Heisenberg
    #                     Uncertainty Device, James Salway discovers the problems 
    #                     of being quantum.</description>
    #                 </book>
    #                 <book id="bk110">
    #                     <author>O'Brien, Tim</author>
    #                     <title>Microsoft .NET: The Programming Bible</title>
    #                     <genre>Computer</genre>
    #                     <price>36.95</price>
    #                     <publish_date>2000-12-09</publish_date>
    #                     <description>Microsoft's .NET initiative is explored in 
    #                     detail in this deep programmer's reference.</description>
    #                 </book>
    #                 <book id="bk111">
    #                     <author>O'Brien, Tim</author>
    #                     <title>MSXML3: A Comprehensive Guide</title>
    #                     <genre>Computer</genre>
    #                     <price>36.95</price>
    #                     <publish_date>2000-12-01</publish_date>
    #                     <description>The Microsoft MSXML3 parser is covered in 
    #                     detail, with attention to XML DOM interfaces, XSLT processing, 
    #                     SAX and more.</description>
    #                 </book>
    #                 <book id="bk112">
    #                     <author>Galos, Mike</author>
    #                     <title>Visual Studio 7: A Comprehensive Guide</title>
    #                     <genre>Computer</genre>
    #                     <price>49.95</price>
    #                     <publish_date>2001-04-16</publish_date>
    #                     <description>Microsoft Visual Studio 7 is explored in depth,
    #                     looking at how Visual Basic, Visual C++, C#, and ASP+ are 
    #                     integrated into a comprehensive development 
    #                     environment.</description>
    #                 </book>
    #                 </catalog>
                
    #             {{ pdf   }}
            
    #         '''
            
            
            
    #         rqMsgFCCreator = RequestMessageFuzzContextCreator()
            
            
            
    #         ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                             apiDiscoveryMethod= "request_message",
    #                             name= "request-message-test",
    #                             hostname='https://example.com',
    #                             port='443',
    #                             authnType=SupportedAuthnType.Anonymous.name,
    #                             fuzzcaseToExec=500,
    #                             openapi3FilePath='',
    #                             requestTextContent= rq
    #                             )
            
    #         self.assertTrue(ok)
    #         self.assertTrue(error == '')
    #         self.assertGreater(len(apicontext.fuzzcaseSets), 0)
            
    #         self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
            
    #         self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": "application/xml"}')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Content-Type": "application/xml"}')
    #         #self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')
    #         #self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')

    #         self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '<?xml version="1.0"?><catalog><book id="bk101"><author>Gambardella, Matthew</author><title>XML Developer\'s Guide</title><genre>Computer</genre><price>44.95</price><publish_date>2000-10-01</publish_date><description>An in-depth look at creating applicationswith XML.</description></book><book id="bk102"><author>Ralls, Kim</author><title>Midnight Rain</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-12-16</publish_date><description>A former architect battles corporate zombies,an evil sorceress, and her own childhood to become queenof the world.</description></book><book id="bk103"><author>Corets, Eva</author><title>Maeve Ascendant</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-11-17</publish_date><description>After the collapse of a nanotechnologysociety in England, the young survivors lay thefoundation for a new society.</description></book><book id="bk104"><author>Corets, Eva</author><title>Oberon\'s Legacy</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-03-10</publish_date><description>In post-apocalypse England, the mysteriousagent known only as Oberon helps to create a new lifefor the inhabitants of London. Sequel to MaeveAscendant.</description></book><book id="bk105"><author>Corets, Eva</author><title>The Sundered Grail</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-09-10</publish_date><description>The two daughters of Maeve, half-sisters,battle one another for control of England. Sequel toOberon\'s Legacy.</description></book><book id="bk106"><author>Randall, Cynthia</author><title>Lover Birds</title><genre>Romance</genre><price>4.95</price><publish_date>2000-09-02</publish_date><description>When Carla meets Paul at an ornithologyconference, tempers fly as feathers get ruffled.</description></book><book id="bk107"><author>Thurman, Paula</author><title>Splish Splash</title><genre>Romance</genre><price>4.95</price><publish_date>2000-11-02</publish_date><description>A deep sea diver finds true love twentythousand leagues beneath the sea.</description></book><book id="bk108"><author>Knorr, Stefan</author><title>Creepy Crawlies</title><genre>Horror</genre><price>4.95</price><publish_date>2000-12-06</publish_date><description>An anthology of horror stories about roaches,centipedes, scorpions  and other insects.</description></book><book id="bk109"><author>Kress, Peter</author><title>Paradox Lost</title><genre>Science Fiction</genre><price>6.95</price><publish_date>2000-11-02</publish_date><description>After an inadvertant trip through a HeisenbergUncertainty Device, James Salway discovers the problemsof being quantum.</description></book><book id="bk110"><author>O\'Brien, Tim</author><title>Microsoft .NET: The Programming Bible</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-09</publish_date><description>Microsoft\'s .NET initiative is explored indetail in this deep programmer\'s reference.</description></book><book id="bk111"><author>O\'Brien, Tim</author><title>MSXML3: A Comprehensive Guide</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-01</publish_date><description>The Microsoft MSXML3 parser is covered indetail, with attention to XML DOM interfaces, XSLT processing,SAX and more.</description></book><book id="bk112"><author>Galos, Mike</author><title>Visual Studio 7: A Comprehensive Guide</title><genre>Computer</genre><price>49.95</price><publish_date>2001-04-16</publish_date><description>Microsoft Visual Studio 7 is explored in depth,looking at how Visual Basic, Visual C++, C#, and ASP+ areintegrated into a comprehensive developmentenvironment.</description></book></catalog>')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '<?xml version="1.0"?><catalog><book id="bk101"><author>Gambardella, Matthew</author><title>XML Developer\'s Guide</title><genre>Computer</genre><price>44.95</price><publish_date>2000-10-01</publish_date><description>An in-depth look at creating applicationswith XML.</description></book><book id="bk102"><author>Ralls, Kim</author><title>Midnight Rain</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-12-16</publish_date><description>A former architect battles corporate zombies,an evil sorceress, and her own childhood to become queenof the world.</description></book><book id="bk103"><author>Corets, Eva</author><title>Maeve Ascendant</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-11-17</publish_date><description>After the collapse of a nanotechnologysociety in England, the young survivors lay thefoundation for a new society.</description></book><book id="bk104"><author>Corets, Eva</author><title>Oberon\'s Legacy</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-03-10</publish_date><description>In post-apocalypse England, the mysteriousagent known only as Oberon helps to create a new lifefor the inhabitants of London. Sequel to MaeveAscendant.</description></book><book id="bk105"><author>Corets, Eva</author><title>The Sundered Grail</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-09-10</publish_date><description>The two daughters of Maeve, half-sisters,battle one another for control of England. Sequel toOberon\'s Legacy.</description></book><book id="bk106"><author>Randall, Cynthia</author><title>Lover Birds</title><genre>Romance</genre><price>4.95</price><publish_date>2000-09-02</publish_date><description>When Carla meets Paul at an ornithologyconference, tempers fly as feathers get ruffled.</description></book><book id="bk107"><author>Thurman, Paula</author><title>Splish Splash</title><genre>Romance</genre><price>4.95</price><publish_date>2000-11-02</publish_date><description>A deep sea diver finds true love twentythousand leagues beneath the sea.</description></book><book id="bk108"><author>Knorr, Stefan</author><title>Creepy Crawlies</title><genre>Horror</genre><price>4.95</price><publish_date>2000-12-06</publish_date><description>An anthology of horror stories about roaches,centipedes, scorpions  and other insects.</description></book><book id="bk109"><author>Kress, Peter</author><title>Paradox Lost</title><genre>Science Fiction</genre><price>6.95</price><publish_date>2000-11-02</publish_date><description>After an inadvertant trip through a HeisenbergUncertainty Device, James Salway discovers the problemsof being quantum.</description></book><book id="bk110"><author>O\'Brien, Tim</author><title>Microsoft .NET: The Programming Bible</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-09</publish_date><description>Microsoft\'s .NET initiative is explored indetail in this deep programmer\'s reference.</description></book><book id="bk111"><author>O\'Brien, Tim</author><title>MSXML3: A Comprehensive Guide</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-01</publish_date><description>The Microsoft MSXML3 parser is covered indetail, with attention to XML DOM interfaces, XSLT processing,SAX and more.</description></book><book id="bk112"><author>Galos, Mike</author><title>Visual Studio 7: A Comprehensive Guide</title><genre>Computer</genre><price>49.95</price><publish_date>2001-04-16</publish_date><description>Microsoft Visual Studio 7 is explored in depth,looking at how Visual Basic, Visual C++, C#, and ASP+ areintegrated into a comprehensive developmentenvironment.</description></book></catalog>')
        
    #         self.assertTrue(len(apicontext.fuzzcaseSets[0].file) == 4)
    
    
    # # parsing body with
    #     # no headers
    #     # multiple breaklines between requestline and body
    #     # multiple files
    #     # xml 
    #     # multiple breaklines between header and body
    # def test_reqmsg_parser_body_no_header_breakline_multiple_files_complex_json(self):
            
          
    #         rq = '''
    #         POST https://example.com/user?name={{username}}&address={{string}}
    #         Content-Type: application/xml
            
            
            
            
    #         {{ file   }}
                
    #             {{ pdf   }}
                
    #             {{ image   }}
                
                
    #             <?xml version="1.0"?>
    #                 <catalog>
    #                 <book id="bk101">
    #                     <author>Gambardella, Matthew</author>
    #                     <title>XML Developer's Guide</title>
    #                     <genre>Computer</genre>
    #                     <price>44.95</price>
    #                     <publish_date>2000-10-01</publish_date>
    #                     <description>An in-depth look at creating applications 
    #                     with XML.</description>
    #                 </book>
    #                 <book id="bk102">
    #                     <author>Ralls, Kim</author>
    #                     <title>Midnight Rain</title>
    #                     <genre>Fantasy</genre>
    #                     <price>5.95</price>
    #                     <publish_date>2000-12-16</publish_date>
    #                     <description>A former architect battles corporate zombies, 
    #                     an evil sorceress, and her own childhood to become queen 
    #                     of the world.</description>
    #                 </book>
    #                 <book id="bk103">
    #                     <author>Corets, Eva</author>
    #                     <title>Maeve Ascendant</title>
    #                     <genre>Fantasy</genre>
    #                     <price>5.95</price>
    #                     <publish_date>2000-11-17</publish_date>
    #                     <description>After the collapse of a nanotechnology 
    #                     society in England, the young survivors lay the 
    #                     foundation for a new society.</description>
    #                 </book>
    #                 <book id="bk104">
    #                     <author>Corets, Eva</author>
    #                     <title>Oberon's Legacy</title>
    #                     <genre>Fantasy</genre>
    #                     <price>5.95</price>
    #                     <publish_date>2001-03-10</publish_date>
    #                     <description>In post-apocalypse England, the mysterious 
    #                     agent known only as Oberon helps to create a new life 
    #                     for the inhabitants of London. Sequel to Maeve 
    #                     Ascendant.</description>
    #                 </book>
    #                 <book id="bk105">
    #                     <author>Corets, Eva</author>
    #                     <title>The Sundered Grail</title>
    #                     <genre>Fantasy</genre>
    #                     <price>5.95</price>
    #                     <publish_date>2001-09-10</publish_date>
    #                     <description>The two daughters of Maeve, half-sisters, 
    #                     battle one another for control of England. Sequel to 
    #                     Oberon's Legacy.</description>
    #                 </book>
    #                 <book id="bk106">
    #                     <author>Randall, Cynthia</author>
    #                     <title>Lover Birds</title>
    #                     <genre>Romance</genre>
    #                     <price>4.95</price>
    #                     <publish_date>2000-09-02</publish_date>
    #                     <description>When Carla meets Paul at an ornithology 
    #                     conference, tempers fly as feathers get ruffled.</description>
    #                 </book>
    #                 <book id="bk107">
    #                     <author>Thurman, Paula</author>
    #                     <title>Splish Splash</title>
    #                     <genre>Romance</genre>
    #                     <price>4.95</price>
    #                     <publish_date>2000-11-02</publish_date>
    #                     <description>A deep sea diver finds true love twenty 
    #                     thousand leagues beneath the sea.</description>
    #                 </book>
    #                 <book id="bk108">
    #                     <author>Knorr, Stefan</author>
    #                     <title>Creepy Crawlies</title>
    #                     <genre>Horror</genre>
    #                     <price>4.95</price>
    #                     <publish_date>2000-12-06</publish_date>
    #                     <description>An anthology of horror stories about roaches,
    #                     centipedes, scorpions  and other insects.</description>
    #                 </book>
    #                 <book id="bk109">
    #                     <author>Kress, Peter</author>
    #                     <title>Paradox Lost</title>
    #                     <genre>Science Fiction</genre>
    #                     <price>6.95</price>
    #                     <publish_date>2000-11-02</publish_date>
    #                     <description>After an inadvertant trip through a Heisenberg
    #                     Uncertainty Device, James Salway discovers the problems 
    #                     of being quantum.</description>
    #                 </book>
    #                 <book id="bk110">
    #                     <author>O'Brien, Tim</author>
    #                     <title>Microsoft .NET: The Programming Bible</title>
    #                     <genre>Computer</genre>
    #                     <price>36.95</price>
    #                     <publish_date>2000-12-09</publish_date>
    #                     <description>Microsoft's .NET initiative is explored in 
    #                     detail in this deep programmer's reference.</description>
    #                 </book>
    #                 <book id="bk111">
    #                     <author>O'Brien, Tim</author>
    #                     <title>MSXML3: A Comprehensive Guide</title>
    #                     <genre>Computer</genre>
    #                     <price>36.95</price>
    #                     <publish_date>2000-12-01</publish_date>
    #                     <description>The Microsoft MSXML3 parser is covered in 
    #                     detail, with attention to XML DOM interfaces, XSLT processing, 
    #                     SAX and more.</description>
    #                 </book>
    #                 <book id="bk112">
    #                     <author>Galos, Mike</author>
    #                     <title>Visual Studio 7: A Comprehensive Guide</title>
    #                     <genre>Computer</genre>
    #                     <price>49.95</price>
    #                     <publish_date>2001-04-16</publish_date>
    #                     <description>Microsoft Visual Studio 7 is explored in depth,
    #                     looking at how Visual Basic, Visual C++, C#, and ASP+ are 
    #                     integrated into a comprehensive development 
    #                     environment.</description>
    #                 </book>
    #                 </catalog>
                
    #             {{ pdf   }}
            
    #         '''
            
            
    #         rqMsgFCCreator = RequestMessageFuzzContextCreator()
        
            
    #         ok, error, apicontext = rqMsgFCCreator.new_fuzzcontext(
    #                             apiDiscoveryMethod= "request_message",
    #                             name= "request-message-test",
    #                             hostname='https://example.com',
    #                             port='443',
    #                             authnType=SupportedAuthnType.Anonymous.name,
    #                             fuzzcaseToExec=500,
    #                             openapi3FilePath='',
    #                             requestTextContent= rq
    #                             )
            
    #         self.assertTrue(ok)
    #         self.assertTrue(error == '')
    #         self.assertGreater(len(apicontext.fuzzcaseSets), 0)
            
    #         self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')
            
    #         self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": "application/xml"}')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Content-Type": "application/xml"}')
    #         #self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')
    #         #self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Authorization": "{{ string }}", "CustomHeader-1": "{{ digit }}", "CustomHeader-2": "{{ filename }}", "CustomHeader-3": "{{ username }}", "Content-Type": "multipart/form-data"}')

    #         self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '<?xml version="1.0"?><catalog><book id="bk101"><author>Gambardella, Matthew</author><title>XML Developer\'s Guide</title><genre>Computer</genre><price>44.95</price><publish_date>2000-10-01</publish_date><description>An in-depth look at creating applicationswith XML.</description></book><book id="bk102"><author>Ralls, Kim</author><title>Midnight Rain</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-12-16</publish_date><description>A former architect battles corporate zombies,an evil sorceress, and her own childhood to become queenof the world.</description></book><book id="bk103"><author>Corets, Eva</author><title>Maeve Ascendant</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-11-17</publish_date><description>After the collapse of a nanotechnologysociety in England, the young survivors lay thefoundation for a new society.</description></book><book id="bk104"><author>Corets, Eva</author><title>Oberon\'s Legacy</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-03-10</publish_date><description>In post-apocalypse England, the mysteriousagent known only as Oberon helps to create a new lifefor the inhabitants of London. Sequel to MaeveAscendant.</description></book><book id="bk105"><author>Corets, Eva</author><title>The Sundered Grail</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-09-10</publish_date><description>The two daughters of Maeve, half-sisters,battle one another for control of England. Sequel toOberon\'s Legacy.</description></book><book id="bk106"><author>Randall, Cynthia</author><title>Lover Birds</title><genre>Romance</genre><price>4.95</price><publish_date>2000-09-02</publish_date><description>When Carla meets Paul at an ornithologyconference, tempers fly as feathers get ruffled.</description></book><book id="bk107"><author>Thurman, Paula</author><title>Splish Splash</title><genre>Romance</genre><price>4.95</price><publish_date>2000-11-02</publish_date><description>A deep sea diver finds true love twentythousand leagues beneath the sea.</description></book><book id="bk108"><author>Knorr, Stefan</author><title>Creepy Crawlies</title><genre>Horror</genre><price>4.95</price><publish_date>2000-12-06</publish_date><description>An anthology of horror stories about roaches,centipedes, scorpions  and other insects.</description></book><book id="bk109"><author>Kress, Peter</author><title>Paradox Lost</title><genre>Science Fiction</genre><price>6.95</price><publish_date>2000-11-02</publish_date><description>After an inadvertant trip through a HeisenbergUncertainty Device, James Salway discovers the problemsof being quantum.</description></book><book id="bk110"><author>O\'Brien, Tim</author><title>Microsoft .NET: The Programming Bible</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-09</publish_date><description>Microsoft\'s .NET initiative is explored indetail in this deep programmer\'s reference.</description></book><book id="bk111"><author>O\'Brien, Tim</author><title>MSXML3: A Comprehensive Guide</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-01</publish_date><description>The Microsoft MSXML3 parser is covered indetail, with attention to XML DOM interfaces, XSLT processing,SAX and more.</description></book><book id="bk112"><author>Galos, Mike</author><title>Visual Studio 7: A Comprehensive Guide</title><genre>Computer</genre><price>49.95</price><publish_date>2001-04-16</publish_date><description>Microsoft Visual Studio 7 is explored in depth,looking at how Visual Basic, Visual C++, C#, and ASP+ areintegrated into a comprehensive developmentenvironment.</description></book></catalog>')
    #         self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '<?xml version="1.0"?><catalog><book id="bk101"><author>Gambardella, Matthew</author><title>XML Developer\'s Guide</title><genre>Computer</genre><price>44.95</price><publish_date>2000-10-01</publish_date><description>An in-depth look at creating applicationswith XML.</description></book><book id="bk102"><author>Ralls, Kim</author><title>Midnight Rain</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-12-16</publish_date><description>A former architect battles corporate zombies,an evil sorceress, and her own childhood to become queenof the world.</description></book><book id="bk103"><author>Corets, Eva</author><title>Maeve Ascendant</title><genre>Fantasy</genre><price>5.95</price><publish_date>2000-11-17</publish_date><description>After the collapse of a nanotechnologysociety in England, the young survivors lay thefoundation for a new society.</description></book><book id="bk104"><author>Corets, Eva</author><title>Oberon\'s Legacy</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-03-10</publish_date><description>In post-apocalypse England, the mysteriousagent known only as Oberon helps to create a new lifefor the inhabitants of London. Sequel to MaeveAscendant.</description></book><book id="bk105"><author>Corets, Eva</author><title>The Sundered Grail</title><genre>Fantasy</genre><price>5.95</price><publish_date>2001-09-10</publish_date><description>The two daughters of Maeve, half-sisters,battle one another for control of England. Sequel toOberon\'s Legacy.</description></book><book id="bk106"><author>Randall, Cynthia</author><title>Lover Birds</title><genre>Romance</genre><price>4.95</price><publish_date>2000-09-02</publish_date><description>When Carla meets Paul at an ornithologyconference, tempers fly as feathers get ruffled.</description></book><book id="bk107"><author>Thurman, Paula</author><title>Splish Splash</title><genre>Romance</genre><price>4.95</price><publish_date>2000-11-02</publish_date><description>A deep sea diver finds true love twentythousand leagues beneath the sea.</description></book><book id="bk108"><author>Knorr, Stefan</author><title>Creepy Crawlies</title><genre>Horror</genre><price>4.95</price><publish_date>2000-12-06</publish_date><description>An anthology of horror stories about roaches,centipedes, scorpions  and other insects.</description></book><book id="bk109"><author>Kress, Peter</author><title>Paradox Lost</title><genre>Science Fiction</genre><price>6.95</price><publish_date>2000-11-02</publish_date><description>After an inadvertant trip through a HeisenbergUncertainty Device, James Salway discovers the problemsof being quantum.</description></book><book id="bk110"><author>O\'Brien, Tim</author><title>Microsoft .NET: The Programming Bible</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-09</publish_date><description>Microsoft\'s .NET initiative is explored indetail in this deep programmer\'s reference.</description></book><book id="bk111"><author>O\'Brien, Tim</author><title>MSXML3: A Comprehensive Guide</title><genre>Computer</genre><price>36.95</price><publish_date>2000-12-01</publish_date><description>The Microsoft MSXML3 parser is covered indetail, with attention to XML DOM interfaces, XSLT processing,SAX and more.</description></book><book id="bk112"><author>Galos, Mike</author><title>Visual Studio 7: A Comprehensive Guide</title><genre>Computer</genre><price>49.95</price><publish_date>2001-04-16</publish_date><description>Microsoft Visual Studio 7 is explored in depth,looking at how Visual Basic, Visual C++, C#, and ASP+ areintegrated into a comprehensive developmentenvironment.</description></book></catalog>')
        
    #         self.assertTrue(len(apicontext.fuzzcaseSets[0].file) == 4)
    
    
    def test_body_multi_breakline_preserved(self):
        
        rq = '''
        POST https://httpbin.org/post
        
        {{
            "
            string,username,password,filename,{{datetime}}
            
            string,username,password,filename,{{datetime}}
            string,username,password,filename,{{datetime}}
            
            string,username,password,filename,{{datetime}}
            
            string,username,password,filename,{{datetime}}
            
            
            
            string,username,password,filename,{{datetime}}
            
            
            
            
            
            
            string,username,password,filename,datetime
            "
            | myfile("batchfile_1.log")
        }}
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
        
        #self.assertTrue(apicontext.fuzzcaseSets[0].verb == 'POST')
        #self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user')

        # self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == 'name={{username}}&password={{password}}')
        # self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == 'name={{username}}&password={{password}}')
        
        print(apicontext.fuzzcaseSets[0].bodyDataTemplate)
        
        
if __name__ == '__main__':
    unittest.main()