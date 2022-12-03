
import unittest
from corpora_context import CorporaContext
from corpora_provider import CorporaProvider

class TestPasswordCorpora(unittest.TestCase):
    
    def __init__(self, methodName: str = ...) -> None:
        self.cp = CorporaProvider()
        super().__init__(methodName)
    
    def setUp(self) -> None:
        
        return super().setUp()
    
    def test_no_expression_in_template(self):
        
        r = '''
                POST https://example.com/comments HTTP/1.1
                Content-Type: application/xml
                Authorization: token xxxx

                <request>
                    
                </request>
            '''
            
        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        
    def test_invalid_expression(self):
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token xxxx

            <request>
                <name>{{ eval() }}</name>
                <time>{{  }}</time>
            </request>
        '''
        
        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok == False)
        self.assertTrue(err != '')
    
    
    def test_inject_corpora_with_file(self):
    
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "file": "{{ eval('file') }}"
            }
        '''                

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')



    def test_inject_corpora_with_valid_my_expression(self):
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "my": "{{ eval( 'my=["journey","to","a","new","world"]' ) }}",
                "my": "{{ eval( 'my=["stranger","things","season","5"]' ) }}",
                "my": "{{ eval( 'my=["stranger"]' ) }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
    def test_inject_corpora_with_invalid_my_missing_end_double_quote(self):
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "my": "{{ eval( 'my=["journey","to","a","new","world]' ) }}",
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertFalse(ok)
        self.assertTrue(err != '')
        
    def test_inject_corpora_with_invalid_my_missing_bracket(self):
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml

            {
                "my": "{{ eval( 'my=["stranger","things","season","5"' ) }}",
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertFalse(ok)
        self.assertTrue(err != '')
    
    
    def test_inject_corpora_with_empty_my(self):
        
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "my": "{{ eval( 'my=[]') }}",
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
            
            
    def test_inject_corpora_with_bool(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "bool": "{{ eval('bool') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
    
    def test_inject_corpora_with_char(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "char": "{{ eval('char') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
    
    def test_inject_corpora_with_image(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "image": "{{ eval('image') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
            
    def test_inject_corpora_with_pdf(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "pdf": "{{ eval('pdf') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
            
    def test_inject_corpora_with_digit(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "digit": "{{ eval('digit') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
            
    def test_inject_corpora_with_password(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                 "password": "{{ eval('password') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
            
    def test_inject_corpora_with_username(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                 "username": "{{ eval('username') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
            
    def test_inject_corpora_with_datetime(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                 "datetime": "{{ eval('datetime') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
            
    def test_inject_corpora_with_date(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                 "date": "{{ eval('date') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
            
    def test_inject_corpora_with_time(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "time": "{{ eval('time') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
            
            
    def test_inject_corpora_with_all_expr_types(self):
            
        r = '''
            POST https://example.com/comments HTTP/1.1
            Content-Type: application/xml
            Authorization: token {{ eval('string') }}

            {
                "my": "{{ eval( 'my=["journey","to","a","new","world"]' ) }}",
                "my": "{{ eval( 'my=["stranger","things","season","5"]' ) }}",
                "my": "{{ eval( 'my=["cool"]' ) }}",
                "string": "{{ eval('string') }}",
                "char": "{{ eval('char') }}",
                "bool": "{{ eval('bool') }}",
                "pdf": "{{ eval('pdf') }}",
                "image": "{{ eval('image') }}",
                "pdf": "{{ eval('pdf') }}",
                "file": "{{ eval('file') }}",
                "password": "{{ eval('password') }}",
                "username": "{{ eval('username') }}",
                "datetime": "{{ eval('datetime') }}",
                "date": "{{ eval('date') }}",
                "time": "{{ eval('time') }}"
            }
        '''

        cc = CorporaContext(self.cp)
        
        ok, err = cc.build(r)
        
        self.assertTrue(ok)
        self.assertTrue(err == '')
        
        self.cp.load_all()
        
        for t in range(100):
            
            ok, err, rtpl = cc.resolve_expr(r)
            
            self.assertTrue(ok)
            self.assertTrue(err == '')
    
        #         ,
        #         ,
        #         ,
        #         ,
        #         ,
        #        ,
        #         ,
        #         ,
        #         "date": "{{ eval('date') }}",
        #         "time": "{{ eval('time') }}"
                
                
if __name__ == '__main__':
    unittest.main()



