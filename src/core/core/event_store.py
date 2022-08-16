import queue

class EventStore:
    
    def __init__(self) -> None:
        
        self.events = []
        self.eventqueue = queue.Queue(maxsize=0)
        
    def append(self, message: str) -> None:
        
        self.eventqueue.put(message)
        
    def _get(self, message: str) -> None:
        
        while True:
            msg = self.eventqueue.get()
            
            self.events.append(msg)
            
    def getEvents(self):
        pass