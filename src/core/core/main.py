'''
Usage:
    main.py
    main.py webserver (start)
    main.py fuzz [--openapi-url=<url>] [--openapi-path=<filepath>] [--rt=<request-text-string>] [--rt-path=<request-text-path>] 
'''

from docopt import docopt

import graphene
from flask import  Flask, jsonify, request, Response

from fuzzcontext import ApiFuzzContext
import atexit
from eventstore import EventStore
from fuzzmanager import FuzzManager

# disable Flask logging
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

#init Flask app
app = Flask(__name__)
host='localhost'
webserverPort = 50001

# runs when program exits
def on_exit():
    eventstore.info("Fuzzie Fuzzer closing")
atexit.register(on_exit)

# declare and init own modules
es = EventStore()
fuzzmanager = FuzzManager(es)


#main entry point and startup
def startup():
    
    args = docopt(__doc__)
    
    global eventstore
    
    if args['webserver']:
        
        
        es.supportExternalClientConsumeEvents = True
        
        es.emitInfo('starting Fuzzie Fuzzer')
        
        es.emitInfo('starting Fuzzie web server')
        es.emitInfo('Fuzzie Fuzzer started')
        
        
        app.run(port=webserverPort, threaded=True)
        
        es.emitInfo("Fuzzie-Fuzzer web server closing")
    else:
        es.emitInfo('Fuzzie Fuzzer started')
    
    

# flask request handlers
@app.route('/api/status', methods = ['GET'])
def get_status():
    
    status = {
        'isReady': True
    }
    
    return jsonify(status)


@app.route('/api/fuzz', methods = ['POST'])
def start_fuzz():
    
    json = request.json
    
    fuzzmanager.fuzz(json)


@app.route('/api/fuzz/progress', methods = ['GET'])
def get_fuzz_progress():
    
    return jsonify({})

@app.route('/api/events', methods = ['GET'])
def get_events():
    
    events = es.getGeneralEventsByBatch()
    
    return jsonify(events)

@app.route('/api/fuzz/report', methods = ['GET'])
def get_fuzz_report():
    
    return jsonify({})


if __name__ == "__main__" or __name__ == "core.main": #name is core.main when run in cmdline python fuzzie-fuzzer.pyz
    startup()

