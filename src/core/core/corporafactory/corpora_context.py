import jinja2
from corpora_provider import CorporaProvider
import re
from user_supplied_corpora import UserSuppliedCorpora
class CorporaContext:
    
    
    def __init__(self, corporaProvider: CorporaProvider) -> None:
        self.cp = corporaProvider
        self.context = {}
    
    def build(self, allDTs: list[str]) -> tuple(bool, str):
        
        # allDTs: all data templates
        
        try:
            
            for dt in allDTs:
                template = jinja2.Template(dt)
                template.render({ 'eval': self.eval_expression })
                
            return True, ''
                
        except Exception as e:
            return False, e
        
        
    def eval_expression(self, expr: str):
        
        if expr is None or expr._undefined_name is None or expr._undefined_name == '':
            raise(Exception('Expression is invalid, detected empty string'))
        
        if expr._undefined_name.startswith('my'):
            self.handle_my_expression(expr)
            return
        
        if expr._undefined_name.startswith('sha256'):
            pass
            return ''
        
        if expr._undefined_name.startswith('base64e'):
            return ''
        
        if expr._undefined_name.startswith('sha256'):
                return ''
        
        if expr._undefined_name.startswith('autonum'):
                return ''
            
        if expr._undefined_name.startswith('uuid'):
                return ''
        
        if expr._undefined_name.startswith('ip'):
                return ''
            
        match expr._undefined_name:
            case 'string':
                if not 'string' in self.context:
                    self.context['string'] = self.cp.stringCorpora
            case 'bool':
                if not 'bool' in self.context:
                    self.context['bool'] = self.cp.boolCorpora
            case 'digit':
                if not 'digit' in self.context:
                    self.context['digit'] = self.cp.digitCorpora
            case 'char':
                if not 'char' in self.context:
                    self.context['char'] = self.cp.charCorpora
            case 'image':
                if not 'image' in self.context:
                    self.context['image'] = self.cp.imageCorpora
            case 'pdf':
                if not 'pdf' in self.context:
                    self.context['pdf'] = self.cp.pdfCorpora
            case 'file':
                if not 'file' in self.context:
                    self.context['file'] = self.cp.pdfCorpora
            case 'datetime':
                if not 'datetime' in self.context:
                    self.context['datetime'] = self.cp.datetimeCorpora
            case 'date':
                if not 'date' in self.context:
                    self.context['date'] = self.cp.datetimeCorpora
            case 'time':
                if not 'time' in self.context:
                    self.context['time'] = self.cp.datetimeCorpora
            case 'username':
               if not 'username' in self.context:
                    self.context['username'] = self.cp.usernameCorpora
            case 'password':
                if not 'password' in self.context:
                    self.context['password'] = self.cp.passwordCorpora
        
            case _:
                return ''
    
    
    def handle_my_expression(self, expr: str):
        
        exprStartIndex = expr.find(':')
        startExpr = expr[exprStartIndex + 1]
        
        usc = UserSuppliedCorpora()
        
        # multiple user supplied string
        if startExpr.startswith('['):
            
           textInbrackets = re.finditer('\[(.*?)\]')
           
           anyEmptStr = any([x for x in textInbrackets if x == ''])
           
           if anyEmptStr:
               self.context[expr] = self.cp.stringCorpora
               return
           
           for t in textInbrackets:
              if t != '':
                usc.load_corpora(t)
            
           self.context[expr] = usc
               
        # single
        else:
            if startExpr == '':
                self.context[expr] = self.cp.stringCorpora
                return
            
            usc.load_corpora(expr)
            
            self.context[expr] = usc
            
    def handle_string_expression(self, expr: str):

        self.context[expr] = self.cp.stringCorpora
        
        
        