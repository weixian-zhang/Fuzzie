import jsonpickle

class Utils:
    def jsone(objDict):
        return jsonpickle.encode(objDict, unpicklable=False)