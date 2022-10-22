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

import asyncio
import uvicorn
from uvicorn.main import Server
# from fastapi import FastAPI, WebSocket
# from ariadne import  make_executable_schema, SubscriptionType
# from ariadne.asgi import GraphQL

import pydantic
# from fastapi import FastAPI, WebSocket
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, WebSocket
from starlette.routing import WebSocketRoute

# from flask import Flask, make_response
# from flask_graphql import GraphQLView
# from graphql_ws.gevent import GeventSubscriptionServer
# from flask_socketio import SocketIO, emit
# from flask_sockets import Sockets

# disable Flask logging
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

# subscription = SubscriptionType()

# @subscription.source("counter")
# async def counter_generator(obj, info):
#     for i in range(5):
#         await asyncio.sleep(1)
#         yield i

# @subscription.field("counter")
# def counter_resolver(count, info):
#     return count + 1


# schema = make_executable_schema(schema, subscription)


    
# routes = [
#     WebSocketRoute("/ws", endpoint=websocket_endpoint),
# ]


app = Starlette()

@app.websocket_route('/ws')
async def websocket_endpoint(websocket):
    await websocket.accept()
    # Process incoming messages
    
    eventstore.set_websocket(websocket)
    
    while True:
        await asyncio.sleep(1)
        # mesg = await websocket.receive_text()
        # await websocket.send_text("hello from server")
    await websocket.close()

# @app.websocket("/graphql/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")





app.mount("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler())) 

#init Flask app
# app = Flask(__name__)
host='localhost'
webserverPort = 50001
# # sockets = Sockets(app)
# socketio = SocketIO(app)

# subscription_server = GeventSubscriptionServer(schema)
# app.app_protocol = lambda environ_path_info: 'graphql-ws'

#init flask-graphql
# app.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view(
#         'graphql',
#         schema=schema,
#         graphiql=True # for having the GraphiQL interface
#     )
# )


# @app.route("/graphiql")
# def graphql_view():
#     return make_response(render_graphiql())


# app.add_url_rule(
#     "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=False)
# )

# subscription_server = GeventSubscriptionServer(schema)
# app.app_protocol = lambda environ_path_info: "graphql-ws"
# # @sockets.route("/subscriptions")
# @socketio.on('countsec')
# def echo_socket(ws):
#     emit('hello from server')
#     # subscription_server.handle(ws)
#     # return []


###################


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
        
        uvicorn.run(app, host="0.0.0.0", port=webserverPort)
        
        #socketio.run(app, host='0.0.0.0', port=webserverPort)
        
        # from gevent import pywsgi
        # from geventwebsocket.handler import WebSocketHandler

        # server = pywsgi.WSGIServer(("", webserverPort), app, handler_class=WebSocketHandler)
        # server.serve_forever()
            
        # app.run(port=webserverPort, threaded=True)
        
        eventstore.emitInfo("Fuzzie-Fuzzer web server closing")
    else:
        eventstore.emitInfo('Fuzzie Fuzzer started')
    

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     eventstore.emitInfo('Fuzzie Core flask-graphql server shutting down')
    
if __name__ == "__main__" or __name__ == "core.main": #name is core.main when run in cmdline python fuzzie-fuzzer.pyz
    startup()

