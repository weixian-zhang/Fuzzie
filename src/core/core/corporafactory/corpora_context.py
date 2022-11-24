import jinja2
from corpora_provider import CorporaProvider
import re

class CorporaContext:
    
    
    def __init__(self, corporaProvider: CorporaProvider) -> None:
        self.cp = corporaProvider
        self.context = {}
    
    def build(self, allDTs: list[str]):
        
        # allDTs: all data templates
        
        for dt in allDTs:
        
            template = jinja2.Template(dt)
            template.render({ 'eval': self.eval_expression })
        
    def eval_expression(self, expr: str):
        
        if expr is None:
            return self.stringGenerator.NextData()
        
        if expr._undefined_name.startswith('my'):
            pass
            return ''
        
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
                return ''
            case 'bool':
                return ''
            case 'digit':
                return ''
            case 'char':
                return ''
            case 'image':
                return ''
            case 'pdf':
                return ''
            case 'datetime':
                return ''
            case 'date':
                return ''
            case 'time':
                return ''
            case 'username':
               if not 'username' in self.context:
                    self.context['username'] = self.cp.usernameCorpora
            case 'password':
                if not 'password' in self.context:
                    self.context['password'] = self.cp.passwordCorpora
            case 'json':
                return ''
        
            case _:
                return ''
    
    
    def handle_my_expression(self, expr: str):
        
        exprStartIndex = expr.find(':')
        startExpr = expr[exprStartIndex + 1]
        
        # multiple user supplied string
        if startExpr.startswith('['):
            
           exprs = re.finditer('\[(.*?)\]')
        
        # single
        else:
            pass
        
        
        