import os, sys
from pathlib import Path
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)

import json
import jinja2

from utils import Utils
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

from backgroundtask_corpora_loader import corporaProvider

class CorporaContext:
    
    
    def __init__(self) -> None:
        self.eventstore = EventStore()
        self.cp = corporaProvider     # CorporaProvider is singleton and already loaded with data during fuzzer startup
        self.context = {}
            
    
    def build_files(self, fileTypes: list[str])-> bool:
        
        for fileType in fileTypes:
            if fileType != '':
                match fileType:
                    case 'image':
                        if not 'image' in self.context:
                            self.context['image'] = self.cp.imageCorpora
                            return True
                    case 'pdf':
                        if not 'pdf' in self.context:
                            self.context['pdf'] = self.cp.pdfCorpora
                            return True
                    case 'file':
                        if not 'file' in self.context:
                            self.context['file'] = self.cp.seclistPayloadCorpora
                            return True
                    case _:
                        return False
            
    
    # will also be use of "parsing" request message. By parsing means build a corpora-context
    # if successful, request message is valid
    def build(self, expression) -> tuple[bool, str]:
        
        if expression == '' or expression == '{}':
            return True, ''
        
        try:
                                    
            if isinstance(expression, str):
                tpl = jinja2.Template(expression)
                tpl.render({ 'eval': self.eval_expression_by_build })
                
            return True, ''
                
        except Exception as e:
            self.eventstore.emitErr(e, 'CorporaContext.build')
            return False, f'Invalid expression: {Utils.errAsText(e)}'
        
    def resolve_wordlistType_to_data(self, expression) -> tuple[bool, str, object]:
        
        try:
            
            template = jinja2.Template(expression)
            rendered = template.render({ 'eval': self.eval_expression_by_injection })
            
            return True, '', rendered
            
        except Exception as e:
            self.eventstore.emitErr(e, 'CorporaContext.resolve_wordlistType_to_data')
            return False, e, ''
    
    # used by openapi 3 web fuzzer only
    def resolve_file(self, expression) -> tuple[bool, str, object]:
        
        try:
        
            if expression not in ['file', 'pdf', 'image']:
                return False, f'Exression {expression} is not a file type', None
            
            provider = self.context[expression]
            if provider != None:
                data = provider.next_corpora()
                return True, '', data
                
            return False, f'Exression {expression} is not a file type', None

        except Exception as e:
            self.eventstore.emitErr(e, 'CorporaContext.resolve_wordlistType_to_data')
            return False, e, ''
        
    
        
    def eval_expression_by_build(self, wordlist_type, my_value = '', my_uniquename='', my_file_content_value='', my_file_content_filename=''):
        
        expression = wordlist_type
        
        originalExpression = f'{{ eval(\'{wordlist_type.strip()}\') }}'
        
        if wordlist_type is None or wordlist_type is None or wordlist_type == '':
            self.context[''] = self.cp.stringCorpora
            return originalExpression
        
        # "my"
        if wordlist_type == 'my':
            
            inputVal = my_value
            
            userSuppliedOrStringCorpora = self.build_MY_expression(inputVal)
            
            key = 'my'
            if my_uniquename != '':
                key = f'{key}_{my_uniquename}'
                
            self.context[expression] = userSuppliedOrStringCorpora
            return originalExpression
        
        # "myFile"
        if wordlist_type == 'myfile':
            corporaContextKey = self.get_myfile_corporacontext_key(my_file_content_filename)
            
            # myfileCorpora is a new instance for every myfile as expression is different
            myfileCorpora = self.cp.new_myfile_corpora(my_file_content_value)
            
            self.context[corporaContextKey] = myfileCorpora
        
        match wordlist_type:
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
            # case 'integer':                         # openapi 3 integer type, using digit corpora
            #     if not 'integer' in self.context:
            #         self.context['integer'] = self.cp.digitCorpora
            #         return originalExpression
            case 'char':
                if not 'char' in self.context:
                    self.context['char'] = self.cp.charCorpora
                    return originalExpression
            case 'filename':
                if not 'filename' in self.context:
                    self.context['filename'] = self.cp.fileNameCorpora
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
                self.eventstore.emitInfo(f'Expression is invalid: "{expression}". Using string corpora instead', 'CorporaContext.eval_expression_by_build')
                return originalExpression
    
    def eval_expression_by_injection(self, wordlist_type, my_value = '', 
                                     my_uniquename='', 
                                     my_file_content_value='', 
                                     my_file_content_filename='',
                                     jsonEscape=True):
        
        try:
            
            if wordlist_type == 'myfile':
                key = self.get_myfile_corporacontext_key(my_file_content_filename)
                provider = self.context[key]
            else:
                provider = self.context[wordlist_type] 
            
            if provider != None:
                data = provider.next_corpora()
                
                if jsonEscape and not self.is_byte_data(data):
                    data = json.dumps(data)
                        
                return data
            else:
                return wordlist_type
            
        except Exception as e:
            self.eventstore.emitErr(e, 'eval_expression_by_injection')
        
    
    # my wordlist type will have "=" sign e.g: my=
    def build_MY_expression(self, expr: str) -> UserSuppliedCorpora:
        
        try:
            
            myInput = expr
            # myInput = expr.removeprefix('my=')
            
            if myInput == '':
                self.eventstore.emitErr('failure to detect "my" input using String corpora instead', 'build_MY_expression')
                return self.cp.stringCorpora

            
            usc = UserSuppliedCorpora()
            
            usc.load_corpora(myInput)
            
            return usc
            
        except Exception as e:
            self.eventstore.emitErr(e, 'build_MY_expression')
            return self.cp .stringCorpora 
   
    def get_myfile_corporacontext_key(self, filename):
        return f'myfile_{filename}'
            
    def handle_string_expression(self, expr: str):

        self.context[expr] = self.cp.stringCorpora
        
    def replace_with_string_corpora(self) -> str:
        data = self.context['string']
        return data
        
    def is_byte_data(self, data):
        try:
            data = data.decode()
            return True
        except (UnicodeDecodeError, AttributeError):
            return False
       
        