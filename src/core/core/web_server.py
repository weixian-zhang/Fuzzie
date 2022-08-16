
from flask import jsonify, request
from flask_classful import FlaskView, route

class WebServer(FlaskView):
              
    
    @route('status', methods = ['GET'])
    def fuzzie_ready(self):
        
        status = {
            'isReady': True
        }
        
        return jsonify(status)
    
    
    @route('fuzz', methods = ['POST'])
    def fuzzie_ready(self):
        
        result = {}
        
        return jsonify(result)
    
    
    @route('fuzzreport', methods = ['GET'])
    def fuzzie_ready(self):
        
        result = {}
        
        return jsonify(result)