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
        
    
    def test_querystring_eval_inject_all_wordlist(self):
        
        rq = '''https://example.com/user
        ?name={{ string }}
        &gender={{ bool) }}
        &age={{ digit) }}
        &age={{ integer }}
        &a={{ char }}
        &a={{ filename }}
        &a={{ datetime }}
        &a={{ date }}
        &a={{ time }}
        &a={{ username }}
        &a={{ password }}
        &a={{ this is a test to prove that I have a very long custom input and Fuzzie accepts it | my }}
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
        &b={{ this is a test to prove that I have a very long custom input and Fuzzie accepts it | my }}
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
        
        self.assertTrue(apicontext.fuzzcaseSets[0].pathDataTemplate == '''https://example.com/user
        ?name={{ eval(\'string\') }}
        &gender={{ eval(\'bool\') }}
        &age={{ eval(\'digit\') }}
        &age={{ eval(\'integer\') }}
        &a={{ eval(\'char\') }}
        &a={{ eval(\'filename\') }}
        &a={{ eval(\'datetime\') }}
        &a={{ eval(\'date\') }}
        &a={{ eval(\'time\') }}
        &a={{ eval(\'username\') }}
        &a={{ eval(\'password\') }}
        &a={{ eval(\'my:this is a test to prove that I have a very long custom input and Fuzzie accepts it\') }}
        &b={{ eval(\'string\') }}
        &b={{ eval(\'bool\') }}
        &b={{ eval(\'digit\') }}
        &b={{ eval(\'integer\') }}
        &b={{ eval(\'char\') }}
        &b={{ eval(\'filename\') }}
        &b={{ eval(\'datetime\') }}
        &b={{ eval(\'date\') }}
        &b={{ eval(\'time\') }}
        &b={{ eval(\'username\') }}
        &b={{ eval(\'password\') }}
        &b={{ eval(\'my:this is a test to prove that I have a very long custom input and Fuzzie accepts it\') }}
        ''')
        
        
if __name__ == '__main__':
    unittest.main()