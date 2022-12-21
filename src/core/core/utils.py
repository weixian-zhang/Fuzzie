import jsonpickle
import shortuuid
from datetime import datetime
import base64

class Utils:
    def jsone(objDict):
        return jsonpickle.encode(objDict, unpicklable=False)
    
    def jsondc(strValue):
        try:
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
        if not Utils.isNoneEmpty(data):
            return
        
        return base64.b64encode(data)