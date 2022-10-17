'''Fuzzie EventStore'''

from multiprocessing import Event
import jsonpickle
from pymitter import EventEmitter
import datetime


class MessageLevel:
    INFO = "INFO"
    ERROR = "ERROR"
    
class Message(object):
    
    def __init__(self, datetime, level, msg, data = None) -> None:
        self.datetime = datetime
        self.level = level
        self.msg = msg
        self.data = data
        
    def json(self):
        return jsonpickle.encode(self, unpicklable=False)
        
 
class EventStore:
    
    GeneralEventTopic = "event_general"
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventStore, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        
        self.ExternalClientConsumeEvents = False
        self.genlogs = []
        self.fuzzProgress = []
        
        self.ee = EventEmitter()
        self.ee.on(EventStore.GeneralEventTopic, self.handleGeneralLogs)
        
    @property
    def supportExternalClientConsumeEvents(self):
        return self.ExternalClientConsumeEvents
    
    @supportExternalClientConsumeEvents.setter
    def supportExternalClientConsumeEvents(self, value):
        self.ExternalClientConsumeEvents = value
        
    def emitInfo(self, message: str, data = "") -> None:
                    
        m = Message(
            datetime.datetime.now(),
            str(MessageLevel.INFO),
            message,
            data
            )
        
        self.ee.emit(EventStore.GeneralEventTopic, m.json())
                
        
    def emitErr(self, error: str, data = "") -> None:
        
        m = Message(
            datetime.datetime.now(),
            str(MessageLevel.ERROR),
            error,
            data
            )
        
        self.ee.emit(EventStore.GeneralEventTopic, m.json())
    
    def emitErr(self, err: any, data = "") -> None:
        
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
        
        self.ee.emit(EventStore.GeneralEventTopic, m.json())
        
    
    def handleGeneralLogs(self, msg: str):
        
        print(msg)
        
        #support external GUI clients to collect logs from fuzzer core
        if self.ExternalClientConsumeEvents:
            self.genlogs.append(msg)
    
    
    #used mainly by external GUI clients to get all general events happening in fuzzer core
    def getGeneralEventsByBatch(self, size = 5) -> list[str]:
        
        if len(self.genlogs) == 0:
            return []
        
        if size > 50:
            size = 50
        
        poplogs = self.genlogs[:size + 1]
        
        del self.genlogs[:size + 1]
        
        return poplogs
