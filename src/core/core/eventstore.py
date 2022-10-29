'''Fuzzie EventStore'''

from enum import Enum
from multiprocessing import Event
import jsonpickle
from pymitter import EventEmitter
from  datetime import datetime
import json
import asyncio

class MessageLevel:
    INFO = "INFO"
    ERROR = "ERROR"
    
class MsgType(Enum):
    AppEvent = 1,
    FuzzEvent = 2

class WebsocketClientMessage:
    def __init__(self, data, msgType: MsgType = MsgType.AppEvent):
        self.timestamp = datetime.now()
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
            datetime.now(),
            str(MessageLevel.INFO),
            message,
            data
            )
        
        self.ee.emit(EventStore.AppEventTopic, m.json())
                
        await self.send_to_ws(message, MsgType.AppEvent)
        
    async def emitErr(self, error: str, data = "") -> None:
        
        m = Message(
            datetime.now(),
            str(MessageLevel.ERROR),
            error,
            data
            )
        
        self.ee.emit(EventStore.AppEventTopic, m.json())
        
        await self.send_to_ws(error, MsgType.AppEvent)
    
    async def emitErr(self, err: Exception, data = "") -> None:
        
        m = None
        
        errMsg = ', '.join([x for x in err.args])
        
        if  isinstance(err, Exception):
            m = Message(
                datetime.now(),
                str(MessageLevel.ERROR),
                errMsg,
                data)
        elif isinstance(err, str):
            m = Message(
                datetime.now(),
                str(MessageLevel.ERROR),
                errMsg,
                data)
        else:
            return
        
        self.ee.emit(EventStore.AppEventTopic, m.json())
        
        await self.send_to_ws(errMsg, MsgType.AppEvent)
        
    
    def handleGeneralLogs(self, msg: str):
        print(msg)
    
    def set_websocket(self, websocket):
        EventStore.websocket = websocket
    
    # send to websocket clients
    async def send_to_ws(self, data: str, msgType: MsgType = MsgType.AppEvent):
        
        try:
            
            # msg = ''
            
            # if not type(data) is str:
            #     msg = jsonpickle.encode(data, unpicklable=False)
        
            m = WebsocketClientMessage(data)
            
            if EventStore.websocket != None:
                if len(EventStore.wsMsgQueue) > 0:
                    while len(EventStore.wsMsgQueue) > 0:
                        await EventStore.websocket.send_text(self.wsMsgQueue.pop())
                    
                await EventStore.websocket.send_text(m.json())
            else:
                EventStore.wsMsgQueue.append(m.json())
        except Exception as e:
            print(e)
        
