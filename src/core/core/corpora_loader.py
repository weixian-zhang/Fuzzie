
from eventstore import EventStore
from corporafactory.corpora_provider import CorporaProvider
from concurrent.futures import ThreadPoolExecutor

es = EventStore()
corporaProvider = CorporaProvider()

def load_corpora_background_done(future):
    es.emitInfo('data loading complete')

# load data background
def load_corpora_background():
    
    es.emitInfo('loading data')
        
    executor = ThreadPoolExecutor()
    
    future = executor.submit(corporaProvider.load_all)
                    
    future.add_done_callback(load_corpora_background_done)