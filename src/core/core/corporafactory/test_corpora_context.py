
import unittest
from corpora_context import CorporaContext
import os, sys
from pathlib import Path

projectDirPath = os.path.dirname(Path(__file__))
parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from utils import Utils

from backgroundtask_corpora_loader import corporaProvider

class TestCorporaContext(unittest.TestCase):
    
    def __init__(self, methodName: str = ...) -> None:
        self.cp = corporaProvider
        #self.cp.load_all()
        super().__init__(methodName)
    
    
    # def test_no_expression_in_template(self):
        
    #     r = '''
    #             POST https://example.com/comments HTTP/1.1
    #             Content-Type: application/xml
    #             Authorization: token xxxx

    #             <request>
                    
    #             </request>
    #         '''
            
    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
        
    # def test_invalid_expression(self):
        
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token xxxx

    #         <request>
    #             <name>{{ eval() }}</name>
    #             <time>{{  }}</time>
    #         </request>
    #     '''
        
    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok == False)
    #     self.assertTrue(err != '')
    
    
    # def test_inject_corpora_with_file(self):
    
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "file": "{{ eval('file') }}"
    #         }
    #     '''                

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')



    # def test_inject_corpora_with_valid_my_expression(self):
        
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "my": "{{ eval( 'my=["journey","to","a","new","world"]' ) }}",
    #             "my": "{{ eval( 'my=["stranger","things","season","5"]' ) }}",
    #             "my": "{{ eval( 'my=["stranger"]' ) }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
    # def test_inject_corpora_with_invalid_my_missing_end_double_quote(self):
        
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "my": "{{ eval("my=journey to the rest of the world") }}",
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertFalse(ok)
    #     self.assertTrue(err != '')
        
    # def test_inject_corpora_with_invalid_my_missing_bracket(self):
        
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml

    #         {
    #             "my": "{{ eval( 'my=stranger things season 5' ) }}",
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertFalse(ok)
    #     self.assertTrue(err != '')
    
    
    # def test_inject_corpora_with_empty_my(self):
        
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "my": "{{ eval( 'my=') }}",
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
            
            
    # def test_inject_corpora_with_bool(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "bool": "{{ eval('bool') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
    
    # def test_inject_corpora_with_char(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "char": "{{ eval('char') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
    
    # def test_inject_corpora_with_image(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "image": "{{ eval('image') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
    
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
            
    # def test_inject_corpora_with_pdf(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "pdf": "{{ eval('pdf') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
            
    # def test_inject_corpora_with_digit(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "digit": "{{ eval('digit') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
    
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
            
    # def test_inject_corpora_with_password(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #              "password": "{{ eval('password') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')

        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
            
    # def test_inject_corpora_with_username(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #              "username": "{{ eval('username') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
            
    # def test_inject_corpora_with_datetime(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #              "datetime": "{{ eval('datetime') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
            
    # def test_inject_corpora_with_date(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #              "date": "{{ eval('date') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
            
    # def test_inject_corpora_with_time(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "time": "{{ eval('time') }}"
    #         }
    #     '''

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(err == '')
            
            
    # def test_inject_corpora_with_all_expr_types(self):
            
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         {
    #             "my": "{{ eval("my=stranger things season 5") }}",
    #             "string": "{{ eval('string') }}",
    #             "char": "{{ eval('char') }}",
    #             "bool": "{{ eval('bool') }}",
    #             "pdf": "{{ eval('pdf') }}",
    #             "image": "{{ eval('image') }}",
    #             "pdf": "{{ eval('pdf') }}",
    #             "file": "{{ eval('file') }}",
    #             "password": "{{ eval('password') }}",
    #             "username": "{{ eval('username') }}",
    #             "datetime": "{{ eval('datetime') }}",
    #             "date": "{{ eval('date') }}",
    #             "time": "{{ eval('time') }}"
    #         }
    #     '''
    

    #     cc = CorporaContext()
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
        
    #     for t in range(100):
            
    #         ok, err, rtpl = cc.resolve_wordlistType_to_data(r)
            
    #         self.assertTrue(ok)
    #         self.assertTrue(rtpl != '')
    
    # POST https://httpbin.org/post
    #
    # {{
    #     "
    #     this is a custom file content
    #     {{ string }} : {{ datetime }}
    #     " | file("a-file.log")
    # }}
    
    #, 
    def test_no_expression_in_template(self):
        
        rq = f'''
            POST https://httpbin.org/post
            
            {{{{ eval('filecontent', args=['this is a custom file content {{string}} : {{datetime}}', 'filename.txt']) }}}}
        '''
            
        cc = CorporaContext()
        
        ok, err = cc.build(rq)
        
        self.assertTrue(ok)
                   
                
if __name__ == '__main__':
    unittest.main()



