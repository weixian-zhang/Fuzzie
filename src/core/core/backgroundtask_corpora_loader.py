
from eventstore import EventStore
from corporafactory.corpora_provider import CorporaProvider
from concurrent.futures import ThreadPoolExecutor
from pubsub import pub
import eventstore

es = EventStore()
corporaProvider = CorporaProvider()

def load_corpora_background_done(future):
    pub.sendMessage(es.CorporaEventTopic, command='corpora_loaded', msgData='')
    es.emitInfo('data loading complete')

# load data background on another thread
def load_corpora_background():
    
    es.emitInfo('loading data')
        
    executor = ThreadPoolExecutor()
    
    future = executor.submit(corporaProvider.load_all)
                    
    future.add_done_callback(load_corpora_background_done)