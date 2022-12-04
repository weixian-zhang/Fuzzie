import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)

import jinja2
import ast

from corpora_provider import CorporaProvider
from user_supplied_corpora import UserSuppliedCorpora
from boolean_corpora import BoolCorpora
from char_corpora import CharCorpora
from datetime_corpora import DateTimeCorpora
from digit_corpora import DigitCorpora
from image_corpora import ImageCorpora
from password_corpora import PasswordCorpora
from pdf_corpora import PDFCorpora
from seclist_payload_corpora import SeclistPayloadCorpora
from string_corpora import StringCorpora
from username_corpora import UsernameCorpora
from eventstore import EventStore

from corpora_loader import corporaProvider

class CorporaContext:
    
    
    def __init__(self) -> None:
        self.es = EventStore()
        self.cp = corporaProvider     # CorporaProvider is singleton and already loaded with data during fuzzer startup
        self.context = {}
            
    
    def build(self, template) -> tuple[bool, str]:
        
        if template == '' or template == '{}':
            return True, ''
        
        try:
            
            if isinstance(template, str):
                template = jinja2.Template(template)
                template.render({ 'eval': self.eval_expression_by_build })
            else:
                for dt in template:
                    template = jinja2.Template(dt)
                    template.render({ 'eval': self.eval_expression_by_build })
                
            return True, ''
                
        except Exception as e:
            self.es.emitErr(e, 'CorporaContext.build')
            return False, f'Invalid expression: {template}'
        
    def resolve_expr(self, expression) -> tuple[bool, str, object]:
        
        try:
            
            template = jinja2.Template(expression)
            rendered = template.render({ 'eval': self.eval_expression_by_injection })
            
            return True, '', rendered
            
        except Exception as e:
            self.es.emitErr(e, 'CorporaContext.resolve_expr')
            return False, e, ''
        
    def eval_expression_by_build(self, expr: str):
        
        expression = expr
        
        originalExpression = f'{{ eval(\'{expr}\') }}'
        
        if expr is None or expression is None or expression == '':
            raise(Exception('Expression is invalid, detected empty string'))
        
        if expression.startswith('my'):
            userSuppliedOrStringCorpora = self.build_MY_expression(expr)
            self.context[expr] = userSuppliedOrStringCorpora
            return originalExpression
        
        if expression.startswith('sha256'):
            return originalExpression
        
        if expression.startswith('base64e'):
            return originalExpression
        
        if expression.startswith('sha256'):
            return originalExpression
        
        if expression.startswith('autonum'):
            return originalExpression
            
        if expression.startswith('uuid'):
            return originalExpression
        
        if expression.startswith('ip'):
            return originalExpression
            
        match expression:
            case 'string':
                if not 'string' in self.context:
                    self.context['string'] = self.cp.stringCorpora
                    return originalExpression
            case 'bool':
                if not 'bool' in self.context:
                    self.context['bool'] = self.cp.boolCorpora
                    return originalExpression
            case 'digit':
                if not 'digit' in self.context:
                    self.context['digit'] = self.cp.digitCorpora
                    return originalExpression
            case 'char':
                if not 'char' in self.context:
                    self.context['char'] = self.cp.charCorpora
                    return originalExpression
            case 'image':
                if not 'image' in self.context:
                    self.context['image'] = self.cp.imageCorpora
                    return originalExpression
            case 'pdf':
                if not 'pdf' in self.context:
                    self.context['pdf'] = self.cp.pdfCorpora
                    return originalExpression
            case 'file':
                if not 'file' in self.context:
                    self.context['file'] = self.cp.seclistPayloadCorpora
                    return originalExpression
            case 'datetime':
                if not 'datetime' in self.context:
                    self.context['datetime'] = self.cp.datetimeCorpora
                    return originalExpression
            case 'date':
                if not 'date' in self.context:
                    self.context['date'] = self.cp.datetimeCorpora
                    return originalExpression
            case 'time':
                if not 'time' in self.context:
                    self.context['time'] = self.cp.datetimeCorpora
                    return originalExpression
            case 'username':
               if not 'username' in self.context:
                    self.context['username'] = self.cp.usernameCorpora
                    return originalExpression
            case 'password':
                if not 'password' in self.context:
                    self.context['password'] = self.cp.passwordCorpora
                    return originalExpression
            case _:
                self.context[expression] = self.cp.stringCorpora
                self.es.emitErr(f'Expression is invalid: "{expression}". Using string corpora instead', 'CorporaContext.eval_expression_by_build')
                return originalExpression
    
    def eval_expression_by_injection(self, expr: str):
        
        expression = expr
        
        # if expr is None or expression is None or expression == '':
        #     raise(Exception('Expression is invalid, detected empty string'))
        
        provider = self.context[expression] 
        
        if provider != None:
            data = provider.next_corpora()
            return data
        else:
            return expression
        
        # if expression.startswith('my'):
            
        #     provider = self.context[expression]
            
        #     if provider is not None and type(provider) is UserSuppliedCorpora:
        #             data = provider.next_corpora()
        #             return data
        #     else:
        #         raise(Exception(f'user supplied input not found in corpora_context {expression}'))
        
        # if expression.startswith('sha256'):
        #     return expr
        
        # if expression.startswith('base64e'):
        #     return expr
        
        # if expression.startswith('sha256'):
        #     return expr
        
        # if expression.startswith('autonum'):
        #     return expr
            
        # if expression.startswith('uuid'):
        #     return expr
        
        # if expression.startswith('ip'):
        #     return expr
            
        # match expression:
        #     case 'string':
        #         provider = self.context[expression]
            
        #         if provider is not None and type(provider) is StringCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'string corpora not found in corpora_context {expression}'))
            
        #     case 'bool':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is BoolCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'bool corpora not found in corpora_context {expression}'))
                    
        #     case 'digit':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is DigitCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'digit corpora not found in corpora_context {expression}'))
                
        #     case 'char':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is CharCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'char corpora not found in corpora_context {expression}'))
                    
        #     case 'image':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is ImageCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'image corpora not found in corpora_context {expression}'))
                    
        #     case 'pdf':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is PDFCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'pdf corpora not found in corpora_context {expression}'))
                    
        #     case 'file':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is SeclistPayloadCorpora:
        #             data = provider.next_corpora()  
        #             return data
        #         else:
        #             raise(Exception(f'file corpora not found in corpora_context {expression}'))
                
        #     case 'datetime':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is DateTimeCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'datetime corpora not found in corpora_context {expression}'))
                
        #     case 'date':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is DateTimeCorpora:
        #             data = provider.next_date_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'date corpora not found in corpora_context {expression}'))
                
        #     case 'time':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is DateTimeCorpora:
        #             data = provider.next_time_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'time corpora not found in corpora_context {expression}'))
                
        #     case 'username':
                
        #         provider = self.context[expression]
            
        #         if provider is not None and type(provider) is UsernameCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'username corpora not found in corpora_context {expression}'))
                
        #     case 'password':
        #         provider = self.context[expression]
        
        #         if provider is not None and type(provider) is PasswordCorpora:
        #             data = provider.next_corpora()
        #             return data
        #         else:
        #             raise(Exception(f'password corpora not found in corpora_context {expression}'))
        #     case _:
        #         return expression
            
    def build_MY_expression(self, expr: str) -> UserSuppliedCorpora:
        
        try:
            exprStartIndex = expr.find('=')
            startExpr = expr[exprStartIndex + 1:]
            
            usc = UserSuppliedCorpora()
            
            usrInputList = ast.literal_eval(startExpr)
            
            # multiple user supplied string
            if type(usrInputList) is list and len(usrInputList) > 0:
            
                for t in usrInputList:
                    if t != '':
                        usc.load_corpora(t)
                        
                return usc
            
            else:
                return self.cp .stringCorpora       # my list is empty use string corpora instead
            
        except Exception as e:
            raise(Exception(f'invalid "my" expression {expr}, {e.msg}. valid expression e.g: my=["fuzzie","is","great"]'))
   
            
    def handle_string_expression(self, expr: str):

        self.context[expr] = self.cp.stringCorpora
        
    def replace_with_string_corpora(self) -> str:
        data = self.context['string']
        return data
        
        
        