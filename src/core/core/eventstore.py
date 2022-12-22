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
from collections import deque

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
    
    websocketClients = {}
    wsMsgQueue = deque( maxlen=5000 )
    AppEventTopic = "AppEventTopic"
    CorporaEventTopic = "corpora_loading"
    CancelFuzzWSTopic = 'fuzz.cancel'
    CancelFuzzingConfirmEventTopic = 'cancel_fuzzing_confirm'
    FuzzStartWSTopic = 'fuzz.start'
    FuzzCompleteWSTopic = 'fuzz.complete'
    InfoWSTopic = 'event.info'
    
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
            self.feedback_client(self.InfoWSTopic, message)

    
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
    
    def add_websocket(self, portId, websocket):
        self.websocketClients[portId] = websocket
    
    def rm_websocket(self, portId):
        if portId in self.websocketClients:
            del self.websocketClients[portId]
    
    # data must be json format
    def feedback_client(self, topic: str, data: str = ''):
        asyncio.run(self.feedback_client_async(topic, data))
    
    # send to websocket clients
    async def feedback_client_async(self, topic: str, data: str):
        
        try:
                   
            m = WebsocketClientMessage(topic, data)
            
            mj = m.json()
            
            if len(self.websocketClients) > 0:
                for portid in self.websocketClients:
                    
                    wsClient = self.websocketClients[portid]
                    
                    while len(self.wsMsgQueue) > 0:
                        
                        msg = self.wsMsgQueue.pop()
                        await wsClient.send_text(msg)
                        
                    await wsClient.send_text(mj)
            else:
                self.wsMsgQueue.append(mj)
                
        except Exception as e:
            self.emitErr(e)
            self.wsMsgQueue.append(mj)
