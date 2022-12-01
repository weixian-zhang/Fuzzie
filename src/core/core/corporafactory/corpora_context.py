import jinja2
from corpora_provider import CorporaProvider
import re
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

import ast

import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)

from eventstore import EventStore

class CorporaContext:
    
    
    def __init__(self, corporaProvider: CorporaProvider) -> None:
        self.es = EventStore()
        self.cp = corporaProvider
        self.context = {}
        
    def next_corpora(self, expression) -> tuple[bool, str, object]:
        
        if expression == '' or expression == None:
            return 
            
    
    def build(self, expression) -> tuple[bool, str]:
        
        # allDTs: all data templates
        
        try:
            
            if isinstance(expression, str):
                template = jinja2.Template(expression)
                template.render({ 'eval': self.eval_expression_by_build })
            else:
                for dt in expression:
                    template = jinja2.Template(dt)
                    template.render({ 'eval': self.eval_expression_by_build })
                
            return True, ''
                
        except Exception as e:
            self.es.emitErr(e)
            return False, f'Invalid expression: {expression}'
        
    def resolve_expr(self, expression) -> tuple[bool, str]:
        
        try:
            
            template = jinja2.Template(expression)
            rendered = template.render({ 'eval': self.eval_expression_by_injection })
            
            return True, '', rendered
            
        except Exception as e:
            self.es.emitErr(e)
            return False, e
        
    def eval_expression_by_build(self, expr: str):
        
        expression = expr
        
        if expr is None or expression is None or expression == '':
            raise(Exception('Expression is invalid, detected empty string'))
        
        if expression.startswith('my'):
            userSuppliedCorpora = self.handle_my_expression(expr)
            self.context[expr] = userSuppliedCorpora
            return expr
        
        if expression.startswith('sha256'):
            return expr
        
        if expression.startswith('base64e'):
            return expr
        
        if expression.startswith('sha256'):
            return expr
        
        if expression.startswith('autonum'):
            return expr
            
        if expression.startswith('uuid'):
            return expr
        
        if expression.startswith('ip'):
            return expr
            
        match expression:
            case 'string':
                if not 'string' in self.context:
                    self.context['string'] = self.cp.stringCorpora
                    return expr
            case 'bool':
                if not 'bool' in self.context:
                    self.context['bool'] = self.cp.boolCorpora
                    return expr
            case 'digit':
                if not 'digit' in self.context:
                    self.context['digit'] = self.cp.digitCorpora
                    return expr
            case 'char':
                if not 'char' in self.context:
                    self.context['char'] = self.cp.charCorpora
                    return expr
            case 'image':
                if not 'image' in self.context:
                    self.context['image'] = self.cp.imageCorpora
                    return expr
            case 'pdf':
                if not 'pdf' in self.context:
                    self.context['pdf'] = self.cp.pdfCorpora
                    return expr
            case 'file':
                if not 'file' in self.context:
                    self.context['file'] = self.cp.seclistPayloadCorpora
                    return expr
            case 'datetime':
                if not 'datetime' in self.context:
                    self.context['datetime'] = self.cp.datetimeCorpora
                    return expr
            case 'date':
                if not 'date' in self.context:
                    self.context['date'] = self.cp.datetimeCorpora
                    return expr
            case 'time':
                if not 'time' in self.context:
                    self.context['time'] = self.cp.datetimeCorpora
                    return expr
            case 'username':
               if not 'username' in self.context:
                    self.context['username'] = self.cp.usernameCorpora
                    return expr
            case 'password':
                if not 'password' in self.context:
                    self.context['password'] = self.cp.passwordCorpora
                    return expr
            case _:
                self.context[expression] = self.cp.stringCorpora
                #raise(Exception(f'Expression is invalid, {expression}'))
    
    def eval_expression_by_injection(self, expr: str):
        
        expression = expr._undefined_name
        
        if expr is None or expression is None or expression == '':
            raise(Exception('Expression is invalid, detected empty string'))
        
        if expression.startswith('my'):
            
            provider = self.context[expression]
            
            if provider is not None and isinstance(provider, UserSuppliedCorpora):
                data = provider.next_corpora()
                return data
            else:
                raise(Exception(f'User supplied corpora not found in corpora context {expression}'))
        
        if expression.startswith('sha256'):
            return expr
        
        if expression.startswith('base64e'):
            return expr
        
        if expression.startswith('sha256'):
            return expr
        
        if expression.startswith('autonum'):
            return expr
            
        if expression.startswith('uuid'):
            return expr
        
        if expression.startswith('ip'):
            return expr
            
        match expression:
            case 'string':
                provider = self.context[expression]
            
                if provider is not None and type(provider) is StringCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'string corpora not found in corpora_context {expression}'))
            
            case 'bool':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is BoolCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'bool corpora not found in corpora_context {expression}'))
                    
            case 'digit':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is DigitCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'digit corpora not found in corpora_context {expression}'))
                
            case 'char':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is CharCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'char corpora not found in corpora_context {expression}'))
                    
            case 'image':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is ImageCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'image corpora not found in corpora_context {expression}'))
                    
            case 'pdf':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is PDFCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'pdf corpora not found in corpora_context {expression}'))
                    
            case 'file':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is SeclistPayloadCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'file corpora not found in corpora_context {expression}'))
                
            case 'datetime':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is DateTimeCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'datetime corpora not found in corpora_context {expression}'))
                
            case 'date':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is DateTimeCorpora:
                    data = provider.dateCorpora()
                    return data
                else:
                    raise(Exception(f'date corpora not found in corpora_context {expression}'))
                
            case 'time':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is DateTimeCorpora:
                    data = provider.timeCorpora()
                    return data
                else:
                    raise(Exception(f'time corpora not found in corpora_context {expression}'))
                
            case 'username':
                
                provider = self.context[expression]
            
                if provider is not None and type(provider) is UsernameCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'username corpora not found in corpora_context {expression}'))
                
            case 'password':
                provider = self.context[expression]
        
                if provider is not None and type(provider) is PasswordCorpora:
                    data = provider.next_corpora()
                    return data
                else:
                    raise(Exception(f'password corpora not found in corpora_context {expression}'))
            
    def handle_my_expression(self, expr: str) -> UserSuppliedCorpora:
        
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
            raise(Exception('invalid "my" expression, did not find any string in list: {expr}'))
               
        # single
        # else:
            
            # if startExpr == '':
            #     self.context[expr] = self.cp.stringCorpora
            #     return
            
            # usc.load_corpora(expr)
            
            # self.context[expr] = usc
            
    def handle_string_expression(self, expr: str):

        self.context[expr] = self.cp.stringCorpora
        
        
        