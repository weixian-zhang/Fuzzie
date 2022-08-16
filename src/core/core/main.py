# usage = '''

# Fuzzie Fuzzer Cli

# Usage:
#     main.py fuzz [--openapi-url=<url>] [--openapi-path=<filepath>] [--rt=<request-text-string>] [--rt-path=<request-text-path>] 
# '''

#from docopt import docopt
from default_fuzzer import DefaultFuzzer
from web_server import WebServer
from flask import Flask

app = Flask(__name__)

WebServer.register(app, route_base='/')

def startup():
    
    print('starting Fuzzie Fuzzer')
    
    print('Fuzzie Fuzzer started')
    
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
    
if __name__ == "__main__":
    startup()
    app.run(host="0.0.0.0", port=50001, debug=True)   