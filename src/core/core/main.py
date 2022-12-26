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

from corpora_loader import load_corpora_background
from starlette_graphql import schema
import asyncio
import uvicorn
from uvicorn.main import Server
import asyncio
from utils import Utils
from pubsub import pub
from threading import Thread
from starlette.middleware.cors import CORSMiddleware 
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import JSONResponse

async def server_error(request, exc):
    return JSONResponse(content={"error": 500}, status_code=exc.status_code)

exception_handlers = {
    #404: not_found,
    500: server_error
}

app = Starlette(exception_handlers=exception_handlers)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

@app.websocket_route("/")
class WebSocketServer(WebSocketEndpoint):
    counter = 0
    encoding = "text"

    #cancel-fuzzing is now done with graphql
    async def on_receive(self, websocket, data):
        pass
            
    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        eventstore.rm_websocket(websocket.client.port)
        eventstore.emitInfo(f'client disconnected from websocket server, close_code {close_code}', 'main.WebSocketServer')
        
    async def on_connect(self, websocket):
        
        try:
            await websocket.accept()
        
            websocket = websocket
            
            eventstore.add_websocket(websocket.client.port, websocket)
            
        except Exception as e:
            eventstore.emitErr(e)
        


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


#main entry point and startup
def start_webserver():
    
    try:
        args = docopt(__doc__)
    
        global eventstore
        
        if args['webserver']:
            
            uvicorn.run(app, 
                        host="0.0.0.0", 
                        port=webserverPort
                        # ssl_keyfile=".\certs\localhost+2-key.pem",
                        # ssl_certfile=".\certs\localhost+2.pem"
                        )
            
            asyncio.run(eventstore.emitInfo("GraphQL server shutting down"))
        else:
            asyncio.run(eventstore.emitInfo('fuzzer started'))
            
    except Exception as e:
        asyncio.run(eventstore.emitErr(e))
    
    

    
if __name__ == "__main__" or __name__ == "core.main": #name is core.main when run in cmdline python fuzzie-fuzzer.pyz
    try:
        
        load_corpora_background()
        
        start_webserver()
        
    except Exception as e:
        asyncio.run(eventstore.emitErr(e))
    

