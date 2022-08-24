'''
Usage:
    main.py
    main.py webserver (start)
    main.py fuzz [--openapi-url=<url>] [--openapi-path=<filepath>] [--rt=<request-text-string>] [--rt-path=<request-text-path>] 
'''

from docopt import docopt
from default_fuzzer import DefaultFuzzer
#from web_server import FuzzerWebServer
from flask import  Flask, jsonify, request

import atexit

app = Flask(__name__)
host='localhost'
webserverPort = 50001

def startup():
    
    print('starting Fuzzie Fuzzer')
    
    args = docopt(__doc__)
    
    if args['webserver']:
        print('starting Fuzzie web server')
        print('Fuzzie Fuzzer started')
        app.run(port=webserverPort)
        print("Fuzzie-Fuzzer web server closing")
    else:
        print('Fuzzie Fuzzer started')
    

def on_exit():
    print("Fuzzie Fuzzer closing")
    
atexit.register(on_exit)


@app.route('/api/status', methods = ['GET'])
def get_status():
    
    status = {
        'isReady': True
    }
    
    return jsonify(status)


@app.route('/api/fuzz', methods = ['POST'])
def start_fuzz():
    
    result = {}
    
    return jsonify(result)


@app.route('/api/fuzzreport', methods = ['GET'])
def get_fuzz_report():
    
    result = {}
    
    return jsonify(result)
    

print(__name__)

if __name__ == "__main__" or __name__ == "core.main": #name is core.main when doing python fuzzie-fuzzer.pyz
    startup()
    
    
    
    
    
    
# def fuzz():
    
#     # args = docopt(usage)
#     # print(args)
    
#     openapiUrl = args['--openapi-url']
#     openapiFilePath = args['--openapi-path']
#     requestTextSingleString = args['--rt']
#     requestTextFilePath = args['--rt-path']
    
#     if (not openapiUrl 
#         and not openapiFilePath 
#         and not requestTextSingleString
#         and not requestTextFilePath):
#         print('fuzzie fuzzer receive empty arguments')
#         return
    
    
#     fuzzie = DefaultFuzzer(openapiUrl=openapiUrl, 
#                            openapiFilePath=openapiFilePath,
#                            requestTextFilePath=requestTextSingleString,
#                            requestTextSingleString=requestTextFilePath)
#     fuzzie.fuzz()

# nodejs forever run python flask app
# https://stackoverflow.com/questions/36465899/how-to-run-flask-server-in-the-background

