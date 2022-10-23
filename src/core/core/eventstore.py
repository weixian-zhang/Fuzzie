'''Fuzzie EventStore'''

from enum import Enum
from multiprocessing import Event
import jsonpickle
from pymitter import EventEmitter
import datetime
import json
import asyncio

class MessageLevel:
    INFO = "INFO"
    ERROR = "ERROR"
    
class MsgType(Enum):
    AppEvent = 1,
    FuzzEvent = 2

class WebsocketClientData:
    def __init__(self, data, msgType: MsgType):
        self.data = data
        self.msgType = msgType.name
    
    def json(self):
        return jsonpickle.encode(self, unpicklable=False)
    
class Message(object):
    
    def __init__(self, datetime, level, msg, data = None) -> None:
        self.datetime = datetime
        self.level = level
        self.msg = msg
        self.data = data
        
    def json(self):
        return jsonpickle.encode(self, unpicklable=False)
        
 
class EventStore:
    
    websocket = None
    wsMsgQueue = []
    AppEventTopic = "AppEventTopic"
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventStore, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        
        self.genlogs = []
        self.fuzzProgress = []
        
        self.ee = EventEmitter()
        self.ee.on(EventStore.AppEventTopic, self.handleGeneralLogs)
        
        
    async def emitInfo(self, message: str, data = "") -> None:
                    
        m = Message(
            datetime.datetime.now(),
            str(MessageLevel.INFO),
            message,
            data
            )
        
        self.ee.emit(EventStore.AppEventTopic, m.json())
                
        await self.send_to_ws(m.json(), MsgType.AppEvent)
        
    async def emitErr(self, error: str, data = "") -> None:
        
        m = Message(
            datetime.datetime.now(),
            str(MessageLevel.ERROR),
            error,
            data
            )
        
        self.ee.emit(EventStore.AppEventTopic, m.json())
        
        await self.send_to_ws(m, MsgType.AppEvent)
    
    async def emitErr(self, err: any, data = "") -> None:
        
        m = None
        
        if  isinstance(err, Exception):
            m = Message(
                datetime.datetime.now(),
                str(MessageLevel.ERROR),
                err.args,
                data)
        elif isinstance(err, str):
            m = Message(
                datetime.datetime.now(),
                str(MessageLevel.ERROR),
                err,
                data)
        else:
            return
        
        self.ee.emit(EventStore.AppEventTopic, m.json())
        
        await self.send_to_ws(m, MsgType.AppEvent)
        
    
    def handleGeneralLogs(self, msg: str):
        print(msg)
    
    def set_websocket(self, websocket):
        EventStore.websocket = websocket
    
    # send to websocket clients
    async def send_to_ws(self, data, msgType: MsgType):
        
        if not type(data) is str:
            data = jsonpickle.encode(data, unpicklable=False)
        
        m = WebsocketClientData(data, msgType)
        
        if EventStore.websocket != None:
            if len(EventStore.wsMsgQueue) > 0:
                while len(EventStore.wsMsgQueue) > 0:
                    await EventStore.websocket.send_text(self.wsMsgQueue.pop())
                
            await EventStore.websocket.send_text(m.json())
        else:
            EventStore.wsMsgQueue.append(m.json())
