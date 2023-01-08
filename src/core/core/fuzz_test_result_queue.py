from eventstore import EventStore
from models.webapi_fuzzcontext import FuzzTestResult

class FuzzTestResultQueue:
    
    resultQueue = []
    
    def enqueue(result: FuzzTestResult):
        FuzzTestResultQueue.resultQueue.append(result)
        
    