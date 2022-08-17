
from flask import jsonify, request
from flask_classful import FlaskView, route

class FuzzerWebServer(FlaskView):
    
    @route('/status', methods = ['GET'])
    def get_status(self):
        
        status = {
            'isReady': True
        }
        
        return jsonify(status)
    
    
    @route('/fuzz', methods = ['POST'])
    def start_fuzz(self):
        
        result = {}
        
        return jsonify(result)
    
    
    @route('/fuzzreport', methods = ['GET'])
    def get_fuzz_report(self):
        
        result = {}
        
        return jsonify(result)