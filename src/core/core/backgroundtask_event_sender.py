import threading
import time
import asyncio
from eventstore import EventStore, WebSocketState

class BackgroundTask_WS_EventSender(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            try:
                if len(EventStore.wsMsgQueue):
                    
                    for portid in EventStore.websocketClients:
                        
                        wsClient = EventStore.websocketClients[portid]
                        
                        if(wsClient.client_state == WebSocketState.CONNECTED):
                        
                            while len(EventStore.wsMsgQueue) > 0:
                                
                                msg = EventStore.wsMsgQueue.popleft()
                                
                                asyncio.run(wsClient.send_text(msg))
                                
                                time.sleep(0.2)
                            
            except Exception as e:
                msg: str = e.args[0]
                print(msg)
                
            time.sleep(0.5)
            

