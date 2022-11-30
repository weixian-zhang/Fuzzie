import jinja2
from corpora_provider import CorporaProvider
import re
from user_supplied_corpora import UserSuppliedCorpora
from boolean_corpora import BoolCorpora
from char_corpora import CharCorpora
from datetime_corpora import DateTimeCorpora
from digit_corpora import DigitCorpora
from file_corpora import FileCorpora
from image_corpora import ImageCorpora
from password_corpora import PasswordCorpora
from pdf_corpora import PDFCorpora
from seclist_payload_corpora import SeclistPayloadCorpora
from string_corpora import StringCorpora
from username_corpora import UsernameCorpora
from file_corpora import FileCorpora

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
            return False, e
        
    def resolve_expr(self, expression) -> tuple[bool, str]:
        
        try:
            
            template = jinja2.Template(expression)
            rendered = template.render({ 'eval': self.eval_expression_by_injection })
            
            return True, '', rendered
            
        except Exception as e:
            self.es.emitErr(e)
            return False, e
        
    def eval_expression_by_build(self, expr: str):
        
        expression = expr._undefined_name
        
        if expr is None or expression is None or expression == '':
            raise(Exception('Expression is invalid, detected empty string'))
        
        if expression.startswith('my'):
            self.handle_my_expression(expr)
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
                    self.context['file'] = self.cp.fileCorpora
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
                raise(Exception(f'Expression is invalid, {expression}'))
    
    def eval_expression_by_injection(self, expr: str):
        
        expression = expr._undefined_name
        
        if expr is None or expression is None or expression == '':
            raise(Exception('Expression is invalid, detected empty string'))
        
        if expression.startswith('my'):
            
            provider = self.context[expression]
            
            if provider is not None and isinstance(provider, UserSuppliedCorpora):
                data = provider.next_corpora()
                return data
            
            raise(Exception(f'User supplied input detected {expression} but a corpora provider is not found in context'))
        
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
                
                raise(Exception(f'User supplied input detected {expression} but a corpora provider is not found in context'))
            
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
                    self.context['file'] = self.cp.fileCorpora
                    return expr
            case 'datetime':
                if not 'datetime' in self.context:
                    provider = self.context[expression]
            
                    if provider is not None and type(provider) is DateTimeCorpora:
                        data = provider.next_corpora()
                        return data
                    
                    raise(Exception(f'User supplied input detected {expression} but a corpora provider is not found in context'))
                
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
                    provider = self.context[expression]
            
                    if provider is not None and type(provider) is UsernameCorpora:
                        data = provider.next_corpora()
                        return data
                    
                    raise(Exception(f'User supplied input detected {expression} but a corpora provider is not found in context'))
                
            case 'password':
                if not 'password' in self.context:
                    self.context['password'] = self.cp.passwordCorpora
                    return expr
            case _:
                raise(Exception(f'Expression is invalid, {expression}'))
            
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
        
        
        