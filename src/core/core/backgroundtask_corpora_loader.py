
from eventstore import EventStore
from corporafactory.corpora_provider import CorporaProvider
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from pubsub import pub
import datetime

es = EventStore()
corporaProvider = CorporaProvider()

def load_corpora_background_done(future):
    
    print(f'data loading completed at {datetime.datetime.now()}')
    
    pub.sendMessage(es.CorporaEventTopic, command='corpora_loaded', msgData='')
    
    es.emitInfo('data loading complete')

# load data background on another thread
def load_corpora_background():
    
    executor =  ThreadPoolExecutor(max_workers=5)
        
    executor.submit(corporaProvider.vacuumSqlite()) 
    
    executor.submit(corporaProvider.load_password_corpora) 
    
    executor.submit(corporaProvider.load_files_corpora)
    
    executor.submit(corporaProvider.load_username_corpora)
    
    executor.submit(corporaProvider.load_string_corpora)
    
    executor.submit(corporaProvider.load_http_path_corpora)
    
    executor.submit(corporaProvider.load_all)
    