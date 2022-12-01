
import unittest
from corpora_context import CorporaContext
from corpora_provider import CorporaProvider

class TestPasswordCorpora(unittest.TestCase):
    
    def __init__(self, methodName: str = ...) -> None:
        self.cp = CorporaProvider()
        super().__init__(methodName)
    
    def setUp(self) -> None:
        
        return super().setUp()
    
    # def test_invalid_expression(self):
        
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token xxxx

    #         <request>
    #             <name>{{ eval('dassa') }}</name>
    #             <time>{{  }}</time>
    #         </request>
    #     '''
        
    #     cc = CorporaContext(self.cp)
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok == False)
    #     self.assertTrue(err != '')
    
    
    # def test_build_context_with_post_xml(self):
        
    #     r = '''
    #         POST https://example.com/comments HTTP/1.1
    #         Content-Type: application/xml
    #         Authorization: token {{ eval('string') }}

    #         <request>
    #             <name>{{ eval('username') }}</name>
    #             <time>{{ eval('datetime') }}</time>
    #         </request>
    #     '''

    #     cc = CorporaContext(self.cp)
        
    #     ok, err = cc.build(r)
        
    #     self.assertTrue(ok)
    #     self.assertTrue(err == '')
    
    def test_inject_corpora_with_post_xml(self):
        
        
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "my": "{{ eval( 'my=["journey","to","a","new","world"]' ) }}",
                "bool": "{{ eval('bool') }}",
                "char": "{{ eval('char') }}",
                "file": "{{ eval('file') }}",
                "image": "{{ eval('image') }}",
                "pdf": "{{ eval('pdf') }}",
                "password": "{{ eval('password') }}"
                "username": "{{ eval('username') }}",
                "datetime": "{{ eval('datetime') }}",
                "date": "{{ eval('date') }}",
                "time": "{{ eval('time') }}",
                "digit": "{{ eval('digit') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        renderedTpl = cc.resolve_expr(r)
        
        print(renderedTpl)
        
if __name__ == '__main__':
    unittest.main()



