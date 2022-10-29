'''
Usage:
    main.py
    main.py webserver (start)
    main.py fuzz [--openapi-url=<url>] [--openapi-path=<filepath>] [--rt=<request-text-string>] [--rt-path=<request-text-path>] 
'''

#https://stackoverflow.com/questions/60899741/python-graphene-subscription-server
# https://github.com/graphql-python/graphql-ws
# https://github.com/graphql-python/graphql-ws/blob/master/examples/flask_gevent/app.py

from time import sleep
from docopt import docopt

from eventstore import EventStore
eventstore = EventStore()
from flaskgql import schema

import json
import asyncio
import uvicorn
from uvicorn.main import Server
import asyncio

from pubsub import pub
# from fastapi import FastAPI, WebSocket
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, WebSocket
from starlette.endpoints import WebSocketEndpoint

app = Starlette()

@app.websocket_route("/ws")
class WebSocketServer(WebSocketEndpoint):
    counter = 0
    encoding = "text"

    async def on_receive(self, websocket, data):
        
        dataCmd = json.loads(data)
        cmd = dataCmd['command']
        
        if cmd == 'cancel_fuzzing':
            pub.sendMessage('command_relay', command='cancel_fuzzing')
    
        #todo: use pubsub library to send command to service manager to cancel fuzzing
        # await websocket.send_text(f"Message text was: {data}")
        
    async def on_connect(self, websocket):
        await websocket.accept()
        eventstore.set_websocket(websocket)

app.mount("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler()))

eventstore.emitInfo('websocket server initialized')

host='localhost'
webserverPort = 50001

# runs when program exits
import atexit
async def on_exit():
    await eventstore.emitInfo("fuzzer stopping")
atexit.register(on_exit)

#main entry point and startup
def startup():
    
    args = docopt(__doc__)
    
    global eventstore
    
    if args['webserver']:
        
        asyncio.run(eventstore.emitInfo('fuzzer started'))
        
        asyncio.run(eventstore.emitInfo('starting GraphQL server'))
        
        uvicorn.run(app, host="0.0.0.0", port=webserverPort)
        
        asyncio.run(eventstore.emitInfo("GraphQL server shutting down"))
    else:
         asyncio.run(eventstore.emitInfo('fuzzer started'))
    

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     eventstore.emitInfo('Fuzzie Core flask-graphql server shutting down')
    
if __name__ == "__main__" or __name__ == "core.main": #name is core.main when run in cmdline python fuzzie-fuzzer.pyz
    startup()

