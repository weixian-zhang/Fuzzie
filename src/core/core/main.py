'''
Usage:
    main.py
    main.py webserver (start)
    main.py fuzz [--openapi-url=<url>] [--openapi-path=<filepath>] [--rt=<request-text-string>] [--rt-path=<request-text-path>] 
'''

from docopt import docopt

from eventstore import EventStore
eventstore = EventStore()

from flask import Flask
from flask_graphql import GraphQLView
from flaskgql import schema

# disable Flask logging
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

#init Flask app
app = Flask(__name__)
host='localhost'
webserverPort = 50001

#init flask-graphql
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

# runs when program exits
import atexit
def on_exit():
    eventstore.emitInfo("Fuzzie stopping")
atexit.register(on_exit)

#main entry point and startup
def startup():
    
    args = docopt(__doc__)
    
    global eventstore
    
    if args['webserver']:
        
        
        eventstore.supportExternalClientConsumeEvents = True
        
        eventstore.emitInfo('starting Fuzzie')
        
        eventstore.emitInfo('starting Fuzzie web server')
        eventstore.emitInfo('Fuzzie Fuzzer started')
        
        
        app.run(port=webserverPort, threaded=True)
        
        eventstore.emitInfo("Fuzzie-Fuzzer web server closing")
    else:
        eventstore.emitInfo('Fuzzie Fuzzer started')
    

@app.teardown_appcontext
def shutdown_session(exception=None):
    eventstore.emitInfo('Fuzzie Core flask-graphql server shutting down')
    
if __name__ == "__main__" or __name__ == "core.main": #name is core.main when run in cmdline python fuzzie-fuzzer.pyz
    startup()

