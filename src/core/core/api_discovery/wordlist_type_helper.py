import jinja2

import os,sys
from pathlib import Path
parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from webapi_fuzzcontext import (WordlistType)

class WordlistTypeHelper:
    
    # integer type is to support OpenApi3, but is same as digit
    def jinja_primitive_wordlist_types_dict() -> dict:
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
            'password': '{{ eval(wordlist_type=\'password\') }}'
        }
        
    def create_jinja_primitive_env(mutate_jinja_filter, jinja_numrange_func):
        env = jinja2.Environment()
        env.filters[WordlistType.mutate] = mutate_jinja_filter
        env.globals[WordlistType.numrange] = jinja_numrange_func
        
        return env
    
    def create_jinja_body_env(mutate_jinja_filter, 
                              myfile_jinja_filter, 
                              jinja_image_func, 
                              jinja_file_func, 
                              jinja_pdf_func,
                              jinja_numrange_func):
        
        env = jinja2.Environment()
        env.filters[WordlistType.mutate] = mutate_jinja_filter
        env.filters[WordlistType.myfile] = myfile_jinja_filter
        env.globals[WordlistType.image] = jinja_image_func
        env.globals[WordlistType.file] = jinja_file_func
        env.globals[WordlistType.pdf] = jinja_pdf_func
        env.globals[WordlistType.numrange] = jinja_numrange_func
        
        return env
        
    