'''Fuzzie EventStore'''

from enum import Enum
from multiprocessing import Event
import jsonpickle
from pymitter import EventEmitter
from  datetime import datetime
from utils import Utils
import asyncio
import nest_asyncio
from pubsub import pub

nest_asyncio.apply()

class MessageLevel:
    INFO = "INFO"
    ERROR = "ERROR"
    
class MsgType(Enum):
    AppEvent = 1,
    FuzzEvent = 2

class WebsocketClientMessage:
    def __init__(self, topic, data): #, msgType: MsgType = MsgType.AppEvent):
        self.timestamp = datetime.now()
        self.data = data
        self.topic = topic
    
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
    CorporaEventTopic = "corpora_loading"
    CancelFuzzingEventTopic = 'cancel_fuzzing'
    FuzzingStartEventTopic = 'fuzzing_start'
    FuzzingStopEventTopic = 'fuzzing_stop'
    InfoEventTopic = 'event.info'
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventStore, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        
        self.pub = pub
        self.genlogs = []
        self.fuzzProgress = []
        
        self.ee = EventEmitter()
        self.ee.on(EventStore.AppEventTopic, self.handleGeneralLogs)
        
        
    def emitInfo(self, message: str, data = "", alsoToClient=True) -> None:
                    
        m = Message(
            datetime.now(),
            str(MessageLevel.INFO),
            message,
            data
            )
        
        self.ee.emit(EventStore.AppEventTopic, m.json())
        
        if alsoToClient:        
            self.feedback_client(self.InfoEventTopic, message)

    
    def emitErr(self, err , data = "") -> None:
        
        m = None
        
        errMsg = ''
        
        if type(err) is str:
            errMsg = err
        else:
           errMsg = Utils.errAsText(err)
        
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
        
        self.feedback_client('event.error', errMsg)
        
    
    def handleGeneralLogs(self, msg: str):
        print(msg)
    
    def set_websocket(self, websocket):
        EventStore.websocket = websocket
    
    # data must be json format
    def feedback_client(self, topic: str, data: str):
        asyncio.run(self.feedback_client_async(topic, data))
    
    # send to websocket clients
    async def feedback_client_async(self, topic: str, data: str):
        
        try:
                   
            m = WebsocketClientMessage(topic, data)
            
            if EventStore.websocket != None:
                if len(EventStore.wsMsgQueue) > 0:
                    while len(EventStore.wsMsgQueue) > 0:
                        await EventStore.websocket.send_text(self.wsMsgQueue.pop())
                    
                await EventStore.websocket.send_text(m.json())
            else:
                EventStore.wsMsgQueue.append(m.json())
                
        except Exception as e:
            EventStore.wsMsgQueue.append(m.json())
            print(e)
