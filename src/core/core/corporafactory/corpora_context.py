import os, sys
from pathlib import Path
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
sys.path.insert(0, os.path.join(core_core_dir, 'models'))

import jinja2
from utils import Utils
from webapi_fuzzcontext import (ApiFuzzCaseSet, WordlistType)
from corpora_provider import CorporaProvider
from user_supplied_corpora import StringMutateCorpora
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
from auto_num_increment_corpora import NumberRangeCorpora
from randomize_items_corpora import RandomItemsCorpora

from backgroundtask_corpora_loader import corporaProvider

class CorporaContext:
    
    def __init__(self) -> None:
        self.eventstore = EventStore()
        self.cp = corporaProvider     # CorporaProvider is singleton and already loaded with data during fuzzer startup
        self.context = {}
        self.tryBuild = False
        self.myfile_wordlist_type = 'myfile'
    
    # try_build_context is used only for parsing request messages from webview
    def try_build_context(self, fcss: list[ApiFuzzCaseSet]) -> tuple([bool, str]):
        try:
            self.build_context(fcss, tryBuild=True)
            return True, ''
        except Exception as e:
            return False, ''
    
    # tryBuild flag is to prevent unnecessary wordlist-type/corpora data loading.
    # Especially type like "numrange" which require user input to generate data on the fly when fuzzing starts
    def build_context(self, fcss: list[ApiFuzzCaseSet], tryBuild=False):
        
        self.tryBuild = tryBuild
        
        try:
            for fcs in fcss:
                
                if not self.isDataTemplateEmpty(fcs.pathDataTemplate):
                    self.build_data_context_from_req_msg(fcs.pathDataTemplate)
                    
                if not self.isDataTemplateEmpty(fcs.querystringDataTemplate):
                    self.build_data_context_from_req_msg(fcs.querystringDataTemplate)
                    
                if not self.isDataTemplateEmpty(fcs.headerDataTemplate):
                    self.build_data_context_from_req_msg(fcs.headerDataTemplate)
                
                if not self.isDataTemplateEmpty(fcs.bodyDataTemplate):
                    self.build_data_context_from_req_msg(fcs.bodyDataTemplate)
                    
                if not self.isDataTemplateEmpty(fcs.graphQLVariableDataTemplate):
                    self.build_data_context_from_req_msg(fcs.graphQLVariableDataTemplate)
                    
                if not self.isDataTemplateEmpty(fcs.fileDataTemplate):
                    self.build_data_context_from_req_msg(fcs.fileDataTemplate)
                    
            return True, ''
                
        except Exception as e:
            return False, Utils.errAsText(e)
           
    
    # will also be use of "parsing" request message. By parsing means build a corpora-context
    # if successful, request message is valid
    def build_data_context_from_req_msg(self, reqMsg) -> tuple[bool, str]:
        
        if reqMsg == '' or reqMsg == '{}':
            return True, ''
        
        try:
                                    
            if isinstance(reqMsg, str):
                tpl = jinja2.Template(reqMsg)
                tpl.render({ 'eval': self.parse_wordlist_type_by_eval_func })
                
            return True, ''
                
        except Exception as e:
            self.eventstore.emitErr(e, 'CorporaContext.build_data_context_from_req_msg')
            return False, f'Invalid expression: {Utils.errAsText(e)}'
        
    def resolve_fuzzdata(self, reqMsg) -> tuple[bool, str, object]:
        
        try:
            
            template = jinja2.Template(reqMsg)
            rendered = template.render({ 'eval': self.resolve_data_by_eval_func })
            
            return True, '', rendered
            
        except Exception as e:
            self.eventstore.emitErr(e, 'CorporaContext.resolve_fuzzdata')
            return False, Utils.errAsText(e), ''
        
    
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
        
    
    def parse_wordlist_type_by_eval_func(self, wordlist_type: str, 
                                         mutate_value = '', 
                                         my_file_content_value='', 
                                         my_file_content_filename='',
                                         autonumStart=1,
                                         autonumEnd=80000,
                                         randomItemsStr = '',):
        
        expression = wordlist_type
        
        originalExpression = f'{{ eval(\'{wordlist_type.strip()}\') }}'
        
        if wordlist_type is None or wordlist_type is None or wordlist_type == '':
            self.context[''] = self.cp.stringCorpora
            return originalExpression
        
        # "mutate"
        if wordlist_type == WordlistType.mutate:
            
            mutateKey = self.get_context_key_for_mutate(mutate_value)
            
            userSuppliedOrStringCorpora = self.build_MY_expression(mutate_value)
                
            self.context[mutateKey] = userSuppliedOrStringCorpora
            
            return
        
        # "myFile"
        if wordlist_type == WordlistType.myfile:
            
            corporaContextKey = self.get_myfile_corporacontext_key(my_file_content_filename)
            
            # myfileCorpora is a new instance for every myfile as expression is different
            myfileCorpora = self.cp.new_myfile_corpora(my_file_content_value)
            
            self.context[corporaContextKey] = myfileCorpora
            
            return
        
        # "numrange"
        if wordlist_type == WordlistType.numrange:
            
            corporaContextKey =f'{wordlist_type}_{autonumStart}_{autonumEnd}'
            
            nic = NumberRangeCorpora(autonumStart, autonumEnd)
            
            if not self.tryBuild:   #load data if this is not parsing requets message
                nic.load_corpora()
            
            self.context[corporaContextKey] = nic
            
            return
        
        # randomize item
        if wordlist_type == WordlistType.random:
            
            corporaContextKey = randomItemsStr
            
            itemArr = randomItemsStr.split(',')
            
            corpora = RandomItemsCorpora(items=itemArr)
            
            self.context[corporaContextKey] = corpora
            
            return
        
        
        match wordlist_type:
            case 'string':
                if not 'string' in self.context:
                    self.context['string'] = self.cp.stringCorpora
                    return
                    #return originalExpression
            case 'xss':
                if not 'xss' in self.context:
                    self.context['xss'] = self.cp.stringCorpora
                    return originalExpression
            case 'sqlinject':
                if not 'sqlinject' in self.context:
                    self.context['sqlinject'] = self.cp.stringCorpora
                    return
                    #return originalExpression
            case 'bool':
                if not 'bool' in self.context:
                    self.context['bool'] = self.cp.boolCorpora
                    return
                    #return originalExpression
            case 'digit':
                if not 'digit' in self.context:
                    self.context['digit'] = self.cp.digitCorpora
                    return
                    #return originalExpression
            case 'char':
                if not 'char' in self.context:
                    self.context['char'] = self.cp.charCorpora
                    return
                    #return originalExpression
            case 'filename':
                if not 'filename' in self.context:
                    self.context['filename'] = self.cp.fileNameCorpora
                    return
                    #return originalExpression
            case 'datetime':
                if not 'datetime' in self.context:
                    self.context['datetime'] = self.cp.datetimeCorpora
                    return
                    #return originalExpression
            case 'date':
                if not 'date' in self.context:
                    self.context['date'] = self.cp.datetimeCorpora
                    return
                    #return originalExpression
            case 'time':
                if not 'time' in self.context:
                    self.context['time'] = self.cp.datetimeCorpora
                    return
                    #return originalExpression
            case 'username':
               if not 'username' in self.context:
                    self.context['username'] = self.cp.usernameCorpora
                    return
                    #return originalExpression
            case 'password':
                if not 'password' in self.context:
                    self.context['password'] = self.cp.passwordCorpora
                    return
                    #return originalExpression
            case WordlistType.httppath:
                if not WordlistType.httppath in self.context:
                    self.context[WordlistType.httppath] = self.cp.httpPathCorpora
                    return
                    #return originalExpression
                
            # image
            case WordlistType.image:
                if not 'image' in self.context:
                    self.context[WordlistType.image] = self.cp.imageCorpora
                    return
                    #return originalExpression
            # pdf          
            case WordlistType.pdf:
                if not WordlistType.pdf in self.context:
                    self.context[WordlistType.pdf] = self.cp.pdfCorpora
                    return
                    #return True
            
            # file  
            case WordlistType.file:
                if not WordlistType.file in self.context:
                    self.context[WordlistType.file] = self.cp.seclistPayloadCorpora
                    return
                    #return True
            
            # no wordlist-type match     
            case _:
                self.context[expression] = self.cp.stringCorpora
                return
                #return originalExpression
    
    def resolve_data_by_eval_func(self, wordlist_type,
                                     mutate_value = '', 
                                     my_file_content_value='', 
                                     my_file_content_filename='',
                                     autonumStart=1,
                                     autonumEnd=100000,
                                     randomItemsStr = ''):
                                     #jsonEscape=True):
        
        try:
            
            data = ''
            
            if wordlist_type == WordlistType.mutate:
                corporaContextKey = self.get_context_key_for_mutate(mutate_value)
                provider: StringMutateCorpora = self.context[corporaContextKey]
            
            elif wordlist_type == WordlistType.myfile:
                key = self.get_myfile_corporacontext_key(my_file_content_filename)
                provider = self.context[key]
                
            elif wordlist_type == WordlistType.xss:
                sc: StringCorpora = self.context[WordlistType.xss]
                data = sc.next_xss_corpora()
                return data
            
            elif wordlist_type == WordlistType.sqlinject:
                sc: StringCorpora = self.context[WordlistType.sqlinject]
                data = sc.next_sqli_corpora()
                return data
            
            elif wordlist_type == WordlistType.numrange:
                corporaContextKey = f'{WordlistType.numrange}_{autonumStart}_{autonumEnd}'
                corpora: NumberRangeCorpora = self.context[corporaContextKey]
                data = corpora.next_corpora()
                return data
            
            elif wordlist_type == WordlistType.random:
                corporaContextKey = randomItemsStr
                corpora = self.context[corporaContextKey]
                data = corpora.next_corpora()
                return data
            
            else:
                # if wordlist_type is not found in Context
                if not self.is_wordlistType_in_context(wordlist_type):
                    self.eventstore.emitErr(Exception('Cannot find wordlist_type in CoorporaContext, could be not "registered" during "build-data-context"'), 'corpora_context.resolve_data_by_eval_func')
                    return self.cp.stringCorpora.next_corpora()
            
                provider = self.context[wordlist_type] 
            
            if provider != None:
                data = provider.next_corpora()
                        
                return data
            else:
                return wordlist_type
            
        except Exception as e:
            self.eventstore.emitErr(e, 'resolve_data_by_eval_func')
        
    
    # my wordlist type will have "=" sign e.g: my=
    def build_MY_expression(self, expr: str) -> StringMutateCorpora:
        
        try:
            
            myInput = expr
            # myInput = expr.removeprefix('my=')
            
            if myInput == '':
                self.eventstore.emitErr('failure to detect "my" input using String corpora instead', 'build_MY_expression')
                return self.cp.stringCorpora

            
            usc = StringMutateCorpora()
            
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
    
    def is_wordlistType_in_context(self, wordlist) -> bool:
        if wordlist in self.context:
            return True
        return False
    
    def get_context_key_for_mutate(self, mutate_value):
       return f'{WordlistType.mutate}_{Utils.sha256(mutate_value)}' 
       
        