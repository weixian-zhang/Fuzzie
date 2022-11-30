
import unittest
from corpora_context import CorporaContext
from corpora_provider import CorporaProvider

class TestPasswordCorpora(unittest.TestCase):
    
    def __init__(self, methodName: str = ...) -> None:
        self.cp = CorporaProvider()
        super().__init__(methodName)
    
    def setUp(self) -> None:
        
        
        
        return super().setUp()
    
    def test_invalid_expression(self):
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token xxxx

            <request>
                <name>{{ eval(dassa) }}</name>
                <time>{{ eval() }}</time>
            </request>
        '''
        
        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok == False)
        self.assertTrue(err != '')
    
    def test_build_context_with_post_xml(self):
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval(string) }}

            <request>
                <name>{{ eval(username) }}</name>
                <time>{{ eval(datetime) }}</time>
            </request>
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
    
    def test_inject_corpora_with_post_xml(self):
        
        self.cp.load_all()
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval(string) }}

            <request>
                <name>{{ eval(username) }}</name>
                <time>{{ eval(datetime) }}</time>
            </request>
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        renderedTpl = cc.resolve_expr(r)
        
        print(renderedTpl)
        
if __name__ == '__main__':
    unittest.main()



