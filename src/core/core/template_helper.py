import jinja2

import os,sys
from pathlib import Path
parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from utils import Utils
from models.webapi_fuzzcontext import (WordlistType)

class TemplateHelper:
    
    def jinja_primitive_wordlists() -> dict:
        return {
            'string': '{{ eval(wordlist_type=\'string\') }}',
            'xss': '{{ eval(wordlist_type=\'xss\') }}',
            'sqlinject': '{{ eval(wordlist_type=\'sqlinject\') }}',
            'bool':  '{{ eval(wordlist_type=\'bool\') }}',
            'digit': '{{ eval(wordlist_type=\'digit\') }}',
            'integer': '{{ eval(wordlist_type=\'integer\') }}',
            'char': '{{ eval(wordlist_type=\'char\') }}',
            'filename': '{{ eval(wordlist_type=\'filename\') }}',
            'datetime': '{{ eval(wordlist_type=\'datetime\') }}',
            'date': '{{ eval(wordlist_type=\'date\') }}',
            'time': '{{ eval(wordlist_type=\'time\') }}',
            'username': '{{ eval(wordlist_type=\'username\') }}',
            'password': '{{ eval(wordlist_type=\'password\') }}',
            'httppath': '{{ eval(wordlist_type=\'httppath\') }}'
        }
        
    def create_jinja_primitive_env(mutate_jinja_filter, 
                                   jinja_numrange_func, 
                                   jinja_randomize_items_filter,
                                   jinja_base64e_filter,
                                   jinja_base64d_filter):
        
        # DebugUndefined retains undefined variables in {{ var }} and not replace unfound variables with nothing
        env = jinja2.Environment(undefined=jinja2.DebugUndefined)   
        
        env.filters[WordlistType.mutate] = mutate_jinja_filter
        env.filters[WordlistType.random] = jinja_randomize_items_filter
        env.filters[WordlistType.base64e] = jinja_base64e_filter
        env.filters[WordlistType.base64d] = jinja_base64d_filter
        
        env.globals[WordlistType.numrange] = jinja_numrange_func
        
        return env
    
    def create_jinja_body_env(mutate_jinja_filter, 
                              myfile_jinja_filter, 
                              jinja_image_func, 
                              jinja_pdf_func,
                              jinja_numrange_func,
                              jinja_randomize_items_filter,
                              jinja_base64e_filter,
                              jinja_base64d_filter):
        
         # DebugUndefined retains undefined variables in {{ var }} and not replace unfound variables with nothing
        env = jinja2.Environment(undefined=jinja2.DebugUndefined)
        
        env.filters[WordlistType.mutate] = mutate_jinja_filter
        env.filters[WordlistType.myfile] = myfile_jinja_filter
        env.filters[WordlistType.random] = jinja_randomize_items_filter
        env.filters[WordlistType.base64e] = jinja_base64e_filter
        env.filters[WordlistType.base64d] = jinja_base64d_filter
        
        env.globals[WordlistType.image] = jinja_image_func
        env.globals[WordlistType.pdf] = jinja_pdf_func
        env.globals[WordlistType.numrange] = jinja_numrange_func
        
        
        return env
    
    
    def add_global_vars(vars: str, tpl: str) -> str:
        if Utils.isNoneEmpty(vars):
            return tpl.strip()
        
        return f'{vars} \n {tpl}'.strip()
    
    
        
    