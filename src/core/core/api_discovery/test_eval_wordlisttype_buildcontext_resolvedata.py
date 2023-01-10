import unittest
import os
import sys
from pathlib import Path

projectDirPath = os.path.dirname(Path(__file__))
parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
corporafactoryDir = os.path.join(parentFolderOfThisFile, 'corporafactory')

sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))
sys.path.insert(0, corporafactoryDir)

from corporafactory.corpora_provider import CorporaProvider
from corporafactory.corpora_context import CorporaContext
from models.webapi_fuzzcontext import SupportedAuthnType
from utils import Utils
from webapi_fuzzcontext import ApiFuzzCaseSet, ApiFuzzContext
from requestmessage_fuzzcontext_creator import RequestMessageFuzzContextCreator

class TestRequestMessageFuzzContextCreator_By_Wordlist_Type(unittest.TestCase):
    
    def __init__(self, methodName: str = ...) -> None:
        self.corporaContext = CorporaContext()
        self.corporaContext.cp.load_all()
        super().__init__(methodName)
        
    def test_MY_input_without_unique_name(self):
        rq = '''
            POST https://httpbin.org/post
            
            {{
                "
                this is my custom input
                with
                break
                line
                " | my
            }}
        '''
        
    def test_MY_input_without_unique_name(self):
        rq = '''
            POST https://httpbin.org/post
            
            {{
                "
                this is my another custom input
                with
                break
                line
                " | my('1')
            }}
        '''
    

    def test_custom_file_content_simple(self):
        
        rq = '''
        POST https://httpbin.org/post
        
        {{
            "
            this is a custom file content \n
            supports with multi breakline \n
            {{ string }} : {{ datetime }} \n
            
            {
                \\"age\\": \\"{{ digit }}\\"
            }
            
            " | myfile("a-file.log")
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
        
        #evalOutput = "{{ eval(wordlist_type='myfile', my_file_content_value='this is a custom file content{{ eval(wordlist_type='string') }} : {{ eval(wordlist_type='datetime') }}', my_file_content_filename='a-file.log') }}"
        #self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == evalOutput)
        
        
        okCP, _ = self.corporaContext.build(apicontext.fuzzcaseSets[0].bodyDataTemplate)
        self.assertTrue(okCP)
        
        # resolve data
        rok, rError, fileContent = self.corporaContext.resolve_wordlistType_to_data(apicontext.fuzzcaseSets[0].bodyDataTemplate)


    def test_custom_file_content_delimited_batchfile(self):
        
        return
        
        rq = '''
        POST https://httpbin.org/post
        
        {{
            "
            this is a custom file content
            {{ string }} : {{ datetime }}
            " | myfile("a-file.log")
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
        
        evalOutput = "{{ eval(wordlist_type=my_file_content, my_file_content_value='this is a custom file content{{ eval(wordlist_type='string') }} : {{ eval(wordlist_type='datetime') }}', my_file_content_filename='a-file.log') }}"
        self.assertTrue(apicontext.fuzzcaseSets[0].bodyDataTemplate == evalOutput)
        
        

if __name__ == '__main__':
    unittest.main()
    
    