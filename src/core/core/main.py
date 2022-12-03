'''
Usage:
    main.py
    main.py webserver (start)
    main.py fuzz [--openapi-url=<url>] [--openapi-path=<filepath>] [--rt=<request-text-string>] [--rt-path=<request-text-path>] 
'''

#https://stackoverflow.com/questions/60899741/python-graphene-subscription-server
# https://github.com/graphql-python/graphql-ws
# https://github.com/graphql-python/graphql-ws/blob/master/examples/flask_gevent/app.py

from multiprocessing import Event
from time import sleep
from docopt import docopt

from eventstore import EventStore
eventstore = EventStore()

from starlette_graphql import schema
from concurrent.futures import ThreadPoolExecutor
import asyncio
import uvicorn
from uvicorn.main import Server
import asyncio
from utils import Utils
from pubsub import pub
# from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, WebSocket
from starlette.endpoints import WebSocketEndpoint

from corporafactory.corpora_provider import CorporaProvider

app = Starlette()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

websocket: WebSocket = None

@app.websocket_route("/ws")
class WebSocketServer(WebSocketEndpoint):
    counter = 0
    encoding = "text"

    async def on_receive(self, websocket, data):
        
        ok, dataCmd = Utils.jsondc(data)
        
        if not ok:
            eventstore.emitErr('invaid json command from websocket client')
            return
         
        cmd = dataCmd['command']
        
        if cmd == 'cancel_fuzzing':
            pub.sendMessage('command_relay', command=eventstore.CancelFuzzingEventTopic)
            eventstore.send_websocket('Fuzzer/main: Fuzzing was cancelled, finishing up some running test cases')
            
            
    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        print(f'Fuzzer/main: client disconnected from websocket server, close_code {close_code}')
        
    async def on_connect(self, websocket):
        await websocket.accept()
        
        websocket = websocket
        
        eventstore.set_websocket(websocket)
        eventstore.send_websocket('Fuzzer/main: client connected to websocket server ')


# init graphql server
app.mount("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler()))

eventstore.emitInfo('websocket server initialized')

host='localhost'
webserverPort = 50001

# runs when program exits
import atexit
def on_exit():
    asyncio.run(eventstore.emitInfo("fuzzer shutting down"))
atexit.register(on_exit)


def load_corpora_background_done(future):
    eventstore.emitInfo('data loading complete')

# load data background
def load_corpora_background():
    
    eventstore.emitInfo('loading data')
    
    cp = CorporaProvider()
        
    executor = ThreadPoolExecutor()
    
    future = executor.submit(cp.load_all)
                    
    future.add_done_callback(load_corpora_background_done)

#main entry point and startup
def startup():
    
    args = docopt(__doc__)
    
    global eventstore
    
    if args['webserver']:
        
        load_corpora_background()
        
        uvicorn.run(app, host="0.0.0.0", port=webserverPort)
        
        asyncio.run(eventstore.emitInfo("GraphQL server shutting down"))
    else:
         asyncio.run(eventstore.emitInfo('fuzzer started'))
    

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     eventstore.emitInfo('Fuzzie Core flask-graphql server shutting down')
    
if __name__ == "__main__" or __name__ == "core.main": #name is core.main when run in cmdline python fuzzie-fuzzer.pyz
    try:
        startup()
    except Exception as e:
        asyncio.run(eventstore.emitErr(e))
    

