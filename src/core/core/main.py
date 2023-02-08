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
from docopt import docopt

from eventstore import EventStore
from backgroundtask_corpora_loader import load_corpora_background
from backgroundtask_event_sender import BackgroundTask_WS_EventSender
from backgroundtask_fuzz_test_result_saver import BackgroundTask_FuzzTest_Result_Saver
from starlette_graphql import schema
import asyncio
import uvicorn
from uvicorn.main import Server
from utils import Utils
from threading import Thread
from starlette.middleware.cors import CORSMiddleware 
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import JSONResponse
import socket, errno

eventstore = EventStore()

# background tasks
wsEventSender = BackgroundTask_WS_EventSender()
wsEventSender.start()
fuzztestResultSaver = BackgroundTask_FuzzTest_Result_Saver()
fuzztestResultSaver.start()

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
    eventstore.emitInfo("fuzzer shutting down")
atexit.register(on_exit)


def is_port_in_use(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(("0.0.0.0", port))
        return False
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
           return True
        else:
            # something else raised the socket.error exception
            print(e)
    finally:
        s.close()
        

#main entry point and startup
def start():
    
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
            
            eventstore.emitInfo("GraphQL server shutting down")
        else:
            eventstore.emitInfo('fuzzer started')
            
    except Exception as e:
        eventstore.emitErr(e)
    
    

    
if __name__ == "__main__" or __name__ == "main": #__name__ == "core.main": #name is core.main when run in cmdline python fuzzie-fuzzer.pyz
    try:
        # check if there is existing fuzzer process already running
        if not is_port_in_use(webserverPort):
            
            load_corpora_background()
            
            start()
        else:
            asyncio.run(eventstore.emitInfo('detected new fuzzer process while existing is running, shutting down new fuzzer'))
        
    except Exception as e:
        asyncio.run(eventstore.emitErr(e))
    

