import jsonpickle
import shortuuid
from datetime import datetime
import base64
import re

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