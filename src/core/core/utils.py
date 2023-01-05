import jsonpickle
import shortuuid
from datetime import datetime
import base64
import re
import xml.etree.ElementTree as elementTree
import jinja2
from jinja2 import environment

class Utils:
    
    def jsone(objDict):
        if objDict is None:
            return ''
        return jsonpickle.encode(objDict, unpicklable=False)
    
    def jsondc(strValue):
        try:
            if strValue == '' or strValue is None:
                return ''
            
            obj = jsonpickle.decode(strValue)
            return True, obj
        except Exception as e:
            return False, {}
        
    def uuid():
        return shortuuid.uuid()
    
    
    def errAsText(err):
        errMsg = ''
        if err != None and err.args is not None and len(err.args) > 0:
            errMsg = ', '.join([x for x in err.args])
            
        return errMsg
    
    def isNoneEmpty(obj) -> bool:
        if obj is None or obj == '':
            return True
        
        return False
    
    
    def datetimeNowStr():
        return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    def b64e(data):
        if Utils.isNoneEmpty(data):
            return ''
        
        b64B = base64.b64encode(bytes(data, "utf-8"))
        
        b64str = b64B.decode('utf-8')
        
        return b64str
    
    def validUrl(url):
        
        regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if re.match(regex, url) is not None:
            return True
        
        return False
    
    
    def isInString(substringToFind, text):
        try:
            idx = text.index(substringToFind)
            return True
        except ValueError as e:
            return False
        
    def isCharsInString(charsToFind: list[str], text):
        try:
            for c in charsToFind:
                if Utils.isInString(c, text): 
                    return True
                else:
                    continue
        except ValueError as e:
            return False
        
    def isXml(value):
        try:
            elementTree.fromstring(value)
        except elementTree.ParseError:
            return False
        return True
    
    # expression example: {{pdf}} {{file}} {{image}}
    # this utility gets pdf, file or image from double curly braces
    def is_filetype_expression(expr: str) -> tuple([bool, str]):
        try:
            exprGroups = re.search('{{(([^}][^}]?|[^}]}?)*)}}', expr)
        
            # tuple length must be 3.
            if exprGroups == None or len(exprGroups.regs) != 3:
                return False, expr
            
            exprType = exprGroups[1].strip()
            
            # fileTypeStrIndexRange = fileType.strip()
            # startIdx = fileTypeStrIndexRange[0]
            # endIdx = fileTypeStrIndexRange[1]
            
            # expressionType = expr[startIdx:endIdx]
            
            for f in  ['file', 'pdf', 'image']:
                if f == exprType:
                    return True, f
            
            return False, exprType
        except Exception as e:
            return False, expr
    
    # integer type is to support OpenApi3, but is same as digit
    def wordlist_types():
        return ['string', 'bool', 'digit', 'integer', 'char', 'filename', 'datetime','date', 'time', 'username', 'password']
        
    # insert eval into wordlist expressions e.g: {{ string }} to {{ eval(string) }}
    # this is for corpora_context to execute eval function to build up the corpora_context base on wordlist-type
    def inject_eval_into_wordlist_expression(expr: str) -> tuple([bool, str, str]):
        
        try:
            
            # insert my wordlist type
            def myWordlist(value):
                return f'{{{{ eval(\'my={value}\') }}}}'
            
            # env = jinja2.Environment()
            environment.DEFAULT_FILTERS['my'] = myWordlist

            tpl = jinja2.Template(expr)
            
            output = tpl.render(
                string='{{ eval(\'string\') }}',
                bool='{{ eval(\'bool\') }}',
                digit='{{ eval(\'digit\') }}',
                integer='{{ eval(\'integer\') }}',
                char='{{ eval(\'char\') }}',
                filename='{{ eval(\'filename\') }}',
                datetime='{{ eval(\'datetime\') }}',
                date='{{ eval(\'date\') }}',
                time='{{ eval(\'time\') }}',
                username='{{ eval(\'username\') }}',
                password='{{ eval(\'password\') }}'
            )                    
                    
            return True, '', output
        
        except Exception as e:
            return False, e,  expr
        
        