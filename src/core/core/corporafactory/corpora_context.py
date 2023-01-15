import os, sys
from pathlib import Path
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
sys.path.insert(0, os.path.join(core_core_dir, 'models'))

import jinja2
from utils import Utils
from webapi_fuzzcontext import (ApiFuzzCaseSet, FuzzCaseSetFile)
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
        
        self.myfile_wordlist_type = 'myfile'
    
    # try_build_context is used only for parsing request messages from webview
    def try_build_context(self, dataTemplate: str) -> tuple([bool, str]):
        try:
            self.build_context_of_req_msg(dataTemplate)
            return True, ''
        except Exception as e:
            return False, ''
    
    def build_context(self, fcss: list[ApiFuzzCaseSet]):
        
        try:
            for fcs in fcss:
                
                if not self.isDataTemplateEmpty(fcs.pathDataTemplate):
                    self.build_context_of_req_msg(fcs.pathDataTemplate)
                    
                if not self.isDataTemplateEmpty(fcs.querystringDataTemplate):
                    self.build_context_of_req_msg(fcs.querystringDataTemplate)
                    
                if not self.isDataTemplateEmpty(fcs.headerDataTemplate):
                    self.build_context_of_req_msg(fcs.headerDataTemplate)
                
                if not self.isDataTemplateEmpty(fcs.bodyDataTemplate):
                    self.build_context_of_req_msg(fcs.bodyDataTemplate)
                    
                if not self.isDataTemplateEmpty(fcs.fileDataTemplate):
                    self.build_context_of_req_msg(fcs.fileDataTemplate)
                    
                return True, ''
                
        except Exception as e:
            return False, Utils.errAsText(e)
           
    
    # will also be use of "parsing" request message. By parsing means build a corpora-context
    # if successful, request message is valid
    def build_context_of_req_msg(self, reqMsg) -> tuple[bool, str]:
        
        if reqMsg == '' or reqMsg == '{}':
            return True, ''
        
        try:
                                    
            if isinstance(reqMsg, str):
                tpl = jinja2.Template(reqMsg)
                tpl.render({ 'eval': self.parse_reqmsg_by_eval_func })
                
            return True, ''
                
        except Exception as e:
            self.eventstore.emitErr(e, 'CorporaContext.build_context_of_req_msg')
            return False, f'Invalid expression: {Utils.errAsText(e)}'
        
    def resolve_fuzzdata(self, reqMsg) -> tuple[bool, str, object]:
        
        try:
            
            template = jinja2.Template(reqMsg)
            rendered = template.render({ 'eval': self.resolve_reqmsg_by_eval_func })
            
            return True, '', rendered
            
        except Exception as e:
            self.eventstore.emitErr(e, 'CorporaContext.resolve_fuzzdata')
            return False, e, ''
        
    
    # get file content for wordlist-file-type
    def resolve_file(self, reqMsg) -> tuple[bool, str, object]:
        
        try:
            
            provider = self.context[reqMsg]
            
            if provider != None:
                data = provider.next_corpora()
                return True, '', data
                
            raise(Exception('corpora provider not found for file type'))

        except Exception as e:
            self.eventstore.emitErr(e, 'CorporaContext.resolve_fuzzdata')
            return False, Utils.errAsText(e), ''
        
    
    def parse_reqmsg_by_eval_func(self, wordlist_type: str, my_value = '', my_uniquename='', my_file_content_value='', my_file_content_filename=''):
        
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
            
            return
            #return originalExpression
        
        # "myFile"
        if wordlist_type == FuzzCaseSetFile.myfile_wordlist_type:
            
            corporaContextKey = self.get_myfile_corporacontext_key(my_file_content_filename)
            
            # myfileCorpora is a new instance for every myfile as expression is different
            myfileCorpora = self.cp.new_myfile_corpora(my_file_content_value)
            
            self.context[corporaContextKey] = myfileCorpora
            
            return
            #return my_file_content_value
        
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
                
            # image
            case FuzzCaseSetFile.image_wordlist_type:
                if not 'image' in self.context:
                    self.context[FuzzCaseSetFile.image_wordlist_type] = self.cp.imageCorpora
                    return originalExpression
            # pdf          
            case FuzzCaseSetFile.pdf_wordlist_type:
                if not FuzzCaseSetFile.pdf_wordlist_type in self.context:
                    self.context[FuzzCaseSetFile.pdf_wordlist_type] = self.cp.pdfCorpora
                    return True
            
            # file  
            case FuzzCaseSetFile.file_wordlist_type:
                if not FuzzCaseSetFile.file_wordlist_type in self.context:
                    self.context[FuzzCaseSetFile.file_wordlist_type] = self.cp.seclistPayloadCorpora
                    return True
            
            # no wordlist-type match     
            case _:
                self.context[expression] = self.cp.stringCorpora
                return originalExpression
    
    def resolve_reqmsg_by_eval_func(self, wordlist_type, my_value = '', 
                                     my_uniquename='', 
                                     my_file_content_value='', 
                                     my_file_content_filename='',
                                     jsonEscape=True):
        
        try:
            
            data = ''
            
            if wordlist_type == 'myfile':
                key = self.get_myfile_corporacontext_key(my_file_content_filename)
                provider = self.context[key]
            else:
                provider = self.context[wordlist_type] 
            
            if provider != None:
                data = provider.next_corpora()
                        
                return data
            else:
                return wordlist_type
            
        except Exception as e:
            self.eventstore.emitErr(e, 'resolve_reqmsg_by_eval_func')
        
    
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
        
    def isDataTemplateEmpty(self, template):
        if template == '' or template == '{}':
            return True
        return False
       
        