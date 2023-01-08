import threading
import time
import asyncio
from fuzz_test_result_queue import FuzzTestResultQueue
from eventstore import EventStore
from db import insert_api_fuzzdatacase, update_casesetrun_summary
eventstore = EventStore()

class BackgroundTask_FuzzTest_Result_Saver(threading.Thread):
    
    
    def run(self,*args,**kwargs):
        while True:
            try:
                if len(FuzzTestResultQueue.resultQueue) > 0:
                    pass
                
                
                            
            except Exception as e:
                eventstore.emitErr(e, 'BackgroundTask_FuzzTest_Result_Saver')
                
            time.sleep(0.5)
            

