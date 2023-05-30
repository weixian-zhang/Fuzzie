
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from utils import Utils
from enum import Enum
from multiprocessing import Event
import jsonpickle
from  datetime import datetime
from pubsub import pub
from collections import deque
from threading import Thread
import time
from starlette_graphene3 import WebSocket, WebSocketState
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
    
    websocketClients: list[WebSocket] = {}
    wsMsgQueue = deque(maxlen=10000)
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
        
        self.logger = logging.getLogger('')
        self.logger.addHandler(AzureLogHandler(
            connection_string='InstrumentationKey=df5dcfcf-b50b-46af-a396-e9554aaa6539;IngestionEndpoint=https://eastasia-0.in.applicationinsights.azure.com/;LiveEndpoint=https://eastasia.livediagnostics.monitor.azure.com/')
        )  
        
        
    def emitInfo(self, message: str, data = "", alsoToClient=True) -> None:
                    
        m = Message(
            datetime.now(),
            str(MessageLevel.INFO),
            message,
            data
            )
        
        print(m.json())

    
    def emitErr(self, err , data = "") -> None:
        
        m = None
        
        errMsg = ''
        
        source = ''
        
        # include source of error raised
        if hasattr(err, 'source'):
            source = err.source

        dataDict = {
            'data': data,
            'source': source
        }     
        
        dataJson = jsonpickle.encode(dataDict, unpicklable=False)          
        
        if type(err) is str:
            errMsg = err
        else:
           errMsg = Utils.errAsText(err)
        
        if  isinstance(err, Exception):
            m = Message(
                datetime.now(),
                str(MessageLevel.ERROR),
                errMsg,
                dataJson)
        elif isinstance(err, str):
            m = Message(
                datetime.now(),
                str(MessageLevel.ERROR),
                errMsg,
                dataJson)
        else:
            return
        
        # TODO: log to Application Insights
        #print(m.json())
        
        self.logger.exception(m.json(), extra={'source': 'fuzzer'})
        
        # may not need to send events over websocket as fuzzer run as child_process,
        # all stdout/stderr will be received by nodejs process module
        #self.feedback_client('event.error', errMsg)
        
    
    def add_websocket(self, portId, websocket):
        self.websocketClients[portId] = websocket
    
    def rm_websocket(self, portId):
        if portId in self.websocketClients:
            del self.websocketClients[portId]
    
    # data must be json format
    # def feedback_client(self, topic: str, data: str = ''):
    #     try:
    #         asyncio.run(self.feedback_client_async(topic, data))
    #     except Exception as e:
    #         self.emitErr(e);
        
    
    # send to websocket clients
    def feedback_client(self, topic: str, data: str = ''): #feedback_client_async(self, topic: str, data: str):
        
        try:
                   
            m = WebsocketClientMessage(topic, data)
            
            mj = m.json()
            
            self.wsMsgQueue.append(mj) #.appendleft(mj)
                
        except Exception as e:
            self.emitErr(e)
            self.wsMsgQueue.append(mj)
            
            
    
