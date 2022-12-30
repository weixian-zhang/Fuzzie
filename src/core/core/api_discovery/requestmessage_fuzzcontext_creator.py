import os,sys
from pathlib import Path

parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from webapi_fuzzcontext import ApiFuzzCaseSet, ApiFuzzContext
from eventstore import EventStore

class RequestMessageFuzzContextCreator:
    
    def __init__(self):
        self.apicontext = None
        self.fuzzcontext = ApiFuzzContext()
        self.eventstore = EventStore()
        
    