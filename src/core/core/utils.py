import jsonpickle

class Utils:
    def jsone(objDict):
        return jsonpickle.encode(objDict, unpicklable=False)
    
    def jsondc(strValue):
        try:
            obj = jsonpickle.decode(strValue)
            return True, obj
        except Exception as e:
            return False, {}
        