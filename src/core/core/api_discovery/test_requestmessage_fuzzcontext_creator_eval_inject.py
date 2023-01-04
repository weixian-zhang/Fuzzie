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

class TestRequestMessageFuzzContextCreator_By_Path(unittest.TestCase):
    
    # def test_path_eval_inject_all_wordlist(self):
        
    #     pathAllWT = 'https://example.com'
        
    #     for x in Utils.wordlist_types():
    #         if x == 'my':
    #             continue
            
    #         pathAllWT = pathAllWT + f'/{{{{ {x} }}}}'
            
    #     # include "my" wordlist
    #     pathAllWT = pathAllWT + f'/{{{{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}}}'
    
    #     rq = f'''
    #        GET {pathAllWT} HTTP/1.1
    #     '''
        
    #     # rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
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
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].pathDataTemplate == '/{{ eval(\'string\') }}/{{ eval(\'bool\') }}/{{ eval(\'digit\') }}/{{ eval(\'integer\') }}/{{ eval(\'char\') }}/{{ eval(\'filename\') }}/{{ eval(\'datetime\') }}/{{ eval(\'date\') }}/{{ eval(\'time\') }}/{{ eval(\'username\') }}/{{ eval(\'password\') }}/{{ eval(\'my:this is a test to prove that I have a very long custom input and Fuzzie accepts it\') }}')
        
        
    # def test_path_eval_inject_repeated_wordlists(self):
        
    #     pathAllWT = 'https://example.com'
        
    #     for x in Utils.wordlist_types():
    #         if x == 'my':
    #             continue
            
    #         pathAllWT = pathAllWT + f'/{{{{ {x} }}}}'
            
    #     pathAllWT = pathAllWT + f'/{{{{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}}}'
        
    #     # repeat
    #     for x in Utils.wordlist_types():
    #         if x == 'my':
    #             continue
            
    #         pathAllWT = pathAllWT + f'/{{{{ {x} }}}}'
            
            
    #     pathAllWT = pathAllWT + f'/{{{{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}}}'
    
    #     rq = f'''
    #        GET {pathAllWT} HTTP/1.1
    #     '''
        
    #     # rqB64 = base64.b64encode(bytes(rq, encoding='utf-8'))
        
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
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].pathDataTemplate == '/{{ eval(\'string\') }}/{{ eval(\'bool\') }}/{{ eval(\'digit\') }}/{{ eval(\'integer\') }}/{{ eval(\'char\') }}/{{ eval(\'filename\') }}/{{ eval(\'datetime\') }}/{{ eval(\'date\') }}/{{ eval(\'time\') }}/{{ eval(\'username\') }}/{{ eval(\'password\') }}/{{ eval(\'my:this is a test to prove that I have a very long custom input and Fuzzie accepts it\') }}/{{ eval(\'string\') }}/{{ eval(\'bool\') }}/{{ eval(\'digit\') }}/{{ eval(\'integer\') }}/{{ eval(\'char\') }}/{{ eval(\'filename\') }}/{{ eval(\'datetime\') }}/{{ eval(\'date\') }}/{{ eval(\'time\') }}/{{ eval(\'username\') }}/{{ eval(\'password\') }}/{{ eval(\'my:this is a test to prove that I have a very long custom input and Fuzzie accepts it\') }}')
        
    
    # def test_querystring_eval_inject_all_wordlist(self):
        
    #     rq = '''https://example.com/user
    #     ?name={{ string }}
    #     &gender={{ bool }}
    #     &age={{ digit }}
    #     &age={{ integer }}
    #     &a={{ char }}
    #     &a={{ filename }}
    #     &a={{ datetime }}
    #     &a={{ date }}
    #     &a={{ time }}
    #     &a={{ username }}
    #     &a={{ password }}
    #     &a={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}
    #     &b={{ string }}
    #     &b={{ bool }}
    #     &b={{ digit }}
    #     &b={{ integer }}
    #     &b={{ char }}
    #     &b={{ filename }}
    #     &b={{ datetime }}
    #     &b={{ date }}
    #     &b={{ time }}
    #     &b={{ username }}
    #     &b={{ password }}
    #     &b={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}
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
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{ string }}&gender={{ bool }}&age={{ digit }}&age={{ integer }}&a={{ char }}&a={{ filename }}&a={{ datetime }}&a={{ date }}&a={{ time }}&a={{ username }}&a={{ password }}&a={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}&b={{ string }}&b={{ bool }}&b={{ digit }}&b={{ integer }}&b={{ char }}&b={{ filename }}&b={{ datetime }}&b={{ date }}&b={{ time }}&b={{ username }}&b={{ password }}&b={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}')
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == '?name={{ eval(\'string\') }}&gender={{ eval(\'bool\') }}&age={{ eval(\'digit\') }}&age={{ eval(\'integer\') }}&a={{ eval(\'char\') }}&a={{ eval(\'filename\') }}&a={{ eval(\'datetime\') }}&a={{ eval(\'date\') }}&a={{ eval(\'time\') }}&a={{ eval(\'username\') }}&a={{ eval(\'password\') }}&a={{ eval(\'my:this is a test to prove that I have a very long custom input and Fuzzie accepts it\') }}&b={{ eval(\'string\') }}&b={{ eval(\'bool\') }}&b={{ eval(\'digit\') }}&b={{ eval(\'integer\') }}&b={{ eval(\'char\') }}&b={{ eval(\'filename\') }}&b={{ eval(\'datetime\') }}&b={{ eval(\'date\') }}&b={{ eval(\'time\') }}&b={{ eval(\'username\') }}&b={{ eval(\'password\') }}&b={{ eval(\'my:this is a test to prove that I have a very long custom input and Fuzzie accepts it\') }}')
        
    
    
    # def test_path_and_querystring_eval_inject_all_wordlist(self):
        
    #     pathAllWT = 'GET https://example.com/user'
        
    #     for x in Utils.wordlist_types():
    #         if x == 'my':
    #             continue
            
    #         pathAllWT = pathAllWT + f'/{{{{ {x} }}}}'
            
    #     pathAllWT = pathAllWT + f'/{{{{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}}}'
        
    #     qs = '''?name={{ string }}
    #     &gender={{ bool }}
    #     &age={{ digit }}
    #     &age={{ integer }}
    #     &a={{ char }}
    #     &a={{ filename }}
    #     &a={{ datetime }}
    #     &a={{ date }}
    #     &a={{ time }}
    #     &a={{ username }}
    #     &a={{ password }}
    #     &a={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}
    #     &b={{ string }}
    #     &b={{ bool }}
    #     &b={{ digit }}
    #     &b={{ integer }}
    #     &b={{ char }}
    #     &b={{ filename }}
    #     &b={{ datetime }}
    #     &b={{ date }}
    #     &b={{ time }}
    #     &b={{ username }}
    #     &b={{ password }}
    #     &b={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}
    #     '''
        
    #     rq = pathAllWT + qs
        
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
        
    #     self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user/{{ string }}/{{ bool }}/{{ digit }}/{{ integer }}/{{ char }}/{{ filename }}/{{ datetime }}/{{ date }}/{{ time }}/{{ username }}/{{ password }}/{{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].pathDataTemplate == "/user/{{ eval('string') }}/{{ eval('bool') }}/{{ eval('digit') }}/{{ eval('integer') }}/{{ eval('char') }}/{{ eval('filename') }}/{{ eval('datetime') }}/{{ eval('date') }}/{{ eval('time') }}/{{ eval('username') }}/{{ eval('password') }}/{{ eval('my:this is a test to prove that I have a very long custom input and Fuzzie accepts it') }}")
    #     self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{ string }}&gender={{ bool }}&age={{ digit }}&age={{ integer }}&a={{ char }}&a={{ filename }}&a={{ datetime }}&a={{ date }}&a={{ time }}&a={{ username }}&a={{ password }}&a={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}&b={{ string }}&b={{ bool }}&b={{ digit }}&b={{ integer }}&b={{ char }}&b={{ filename }}&b={{ datetime }}&b={{ date }}&b={{ time }}&b={{ username }}&b={{ password }}&b={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}')
    #     self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == "?name={{ eval('string') }}&gender={{ eval('bool') }}&age={{ eval('digit') }}&age={{ eval('integer') }}&a={{ eval('char') }}&a={{ eval('filename') }}&a={{ eval('datetime') }}&a={{ eval('date') }}&a={{ eval('time') }}&a={{ eval('username') }}&a={{ eval('password') }}&a={{ eval('my:this is a test to prove that I have a very long custom input and Fuzzie accepts it') }}&b={{ eval('string') }}&b={{ eval('bool') }}&b={{ eval('digit') }}&b={{ eval('integer') }}&b={{ eval('char') }}&b={{ eval('filename') }}&b={{ eval('datetime') }}&b={{ eval('date') }}&b={{ eval('time') }}&b={{ eval('username') }}&b={{ eval('password') }}&b={{ eval('my:this is a test to prove that I have a very long custom input and Fuzzie accepts it') }}")
    
    
    def test_path_and_querystring_eval_inject_all_wordlist(self):
        
        pathAllWT = 'GET https://example.com/user'
        
        for x in Utils.wordlist_types():
            if x == 'my':
                continue
            
            pathAllWT = pathAllWT + f'/{{{{ {x} }}}}'
            
        pathAllWT = pathAllWT + f'/{{{{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}}}'
        
        qs = '''?name={{ string }}
        &gender={{ bool }}
        &age={{ digit }}
        &age={{ integer }}
        &a={{ char }}
        &a={{ filename }}
        &a={{ datetime }}
        &a={{ date }}
        &a={{ time }}
        &a={{ username }}
        &a={{ password }}
        &a={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}
        &b={{ string }}
        &b={{ bool }}
        &b={{ digit }}
        &b={{ integer }}
        &b={{ char }}
        &b={{ filename }}
        &b={{ datetime }}
        &b={{ date }}
        &b={{ time }}
        &b={{ username }}
        &b={{ password }}
        &b={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}
        Content-Type: application/json
        custom-header1: {{ string }}
        custom-header2: {{ bool }}
        custom-header3: {{ digit }}
        custom-header4: {{ integer }}
        custom-header5: {{ char }}
        custom-header6: {{ filename }}
        custom-header7: {{ datetime }}
        custom-header8: {{ date }}
        custom-header9: {{ time }}
        custom-header10: {{ username }}
        custom-header11: {{ password }}
        custom-header12: {{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }} 
        
        {
                "string": "{{ string }}",
                "bool": "{{ bool }}",
                "digit": "{{ digit }}",
                "integer": "{{ integer }}",
                "char": "{{ char }}",
                "filename": "{{ filename }}",
                "datetime": "{{ datetime }}",
                "date": "{{ date }}",
                "time": "{{ time }}",
                "username": "{{ username }}",
                "password": "{{ password }}",
                "custom-inputs": "{{ "a custom input to be mutated" | my }}"
            }
        
        '''
        
        rq = pathAllWT + qs
        
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
        
        self.assertTrue(apicontext.fuzzcaseSets[0].path == '/user/{{ string }}/{{ bool }}/{{ digit }}/{{ integer }}/{{ char }}/{{ filename }}/{{ datetime }}/{{ date }}/{{ time }}/{{ username }}/{{ password }}/{{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}')
        self.assertTrue(apicontext.fuzzcaseSets[0].pathDataTemplate == "/user/{{ eval('string') }}/{{ eval('bool') }}/{{ eval('digit') }}/{{ eval('integer') }}/{{ eval('char') }}/{{ eval('filename') }}/{{ eval('datetime') }}/{{ eval('date') }}/{{ eval('time') }}/{{ eval('username') }}/{{ eval('password') }}/{{ eval('my:this is a test to prove that I have a very long custom input and Fuzzie accepts it') }}")
        
        self.assertTrue(apicontext.fuzzcaseSets[0].headerNonTemplate == '{"Content-Type": "application/json", "custom-header1": "{{ string }}", "custom-header2": "{{ bool }}", "custom-header3": "{{ digit }}", "custom-header4": "{{ integer }}", "custom-header5": "{{ char }}", "custom-header6": "{{ filename }}", "custom-header7": "{{ datetime }}", "custom-header8": "{{ date }}", "custom-header9": "{{ time }}", "custom-header10": "{{ username }}", "custom-header11": "{{ password }}", "custom-header12": "{{ \\"this is a test to prove that I have a very long custom input and Fuzzie accepts it\\" | my }}"}')
        self.assertTrue(apicontext.fuzzcaseSets[0].headerDataTemplate == '{"Content-Type": "application/json", "custom-header1": "{{ eval(\'string\') }}", "custom-header2": "{{ eval(\'bool\') }}", "custom-header3": "{{ eval(\'digit\') }}", "custom-header4": "{{ eval(\'integer\') }}", "custom-header5": "{{ eval(\'char\') }}", "custom-header6": "{{ eval(\'filename\') }}", "custom-header7": "{{ eval(\'datetime\') }}", "custom-header8": "{{ eval(\'date\') }}", "custom-header9": "{{ eval(\'time\') }}", "custom-header10": "{{ eval(\'username\') }}", "custom-header11": "{{ eval(\'password\') }}", "custom-header12": "{{ eval(\'my:this is a test to prove that I have a very long custom input and Fuzzie accepts it\') }}"}' )
        
        self.assertTrue(apicontext.fuzzcaseSets[0].bodyNonTemplate == '{"string": "{{ string }}","bool": "{{ bool }}","digit": "{{ digit }}","integer": "{{ integer }}","char": "{{ char }}","filename": "{{ filename }}","datetime": "{{ datetime }}","date": "{{ date }}","time": "{{ time }}","username": "{{ username }}","password": "{{ password }}","custom-inputs": "{{ "a custom input to be mutated" | my }}"}')
        self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == '{"string": "{{ eval(\'string\') }}","bool": "{{ eval(\'bool\') }}","digit": "{{ eval(\'digit\') }}","integer": "{{ eval(\'integer\') }}","char": "{{ eval(\'char\') }}","filename": "{{ eval(\'filename\') }}","datetime": "{{ eval(\'datetime\') }}","date": "{{ eval(\'date\') }}","time": "{{ eval(\'time\') }}","username": "{{ eval(\'username\') }}","password": "{{ eval(\'password\') }}","custom-inputs": "{{ eval(\'my:a custom input to be mutated\') }}"}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringNonTemplate == '?name={{ string }}&gender={{ bool }}&age={{ digit }}&age={{ integer }}&a={{ char }}&a={{ filename }}&a={{ datetime }}&a={{ date }}&a={{ time }}&a={{ username }}&a={{ password }}&a={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}&b={{ string }}&b={{ bool }}&b={{ digit }}&b={{ integer }}&b={{ char }}&b={{ filename }}&b={{ datetime }}&b={{ date }}&b={{ time }}&b={{ username }}&b={{ password }}&b={{ "this is a test to prove that I have a very long custom input and Fuzzie accepts it" | my }}')
        self.assertTrue(apicontext.fuzzcaseSets[0].querystringDataTemplate == "?name={{ eval('string') }}&gender={{ eval('bool') }}&age={{ eval('digit') }}&age={{ eval('integer') }}&a={{ eval('char') }}&a={{ eval('filename') }}&a={{ eval('datetime') }}&a={{ eval('date') }}&a={{ eval('time') }}&a={{ eval('username') }}&a={{ eval('password') }}&a={{ eval('my:this is a test to prove that I have a very long custom input and Fuzzie accepts it') }}&b={{ eval('string') }}&b={{ eval('bool') }}&b={{ eval('digit') }}&b={{ eval('integer') }}&b={{ eval('char') }}&b={{ eval('filename') }}&b={{ eval('datetime') }}&b={{ eval('date') }}&b={{ eval('time') }}&b={{ eval('username') }}&b={{ eval('password') }}&b={{ eval('my:this is a test to prove that I have a very long custom input and Fuzzie accepts it') }}")       
        
if __name__ == '__main__':
    unittest.main()