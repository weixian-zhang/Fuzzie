# act as a Application Layer to coordinate other operations like FuzzContextCreator, Sqlalchemy CRUDs

from api_discovery.openapi3_discoverer import OpenApi3ApiDiscover
from api_discovery.openapi3_fuzzcontext_creator import OpenApi3FuzzContextCreator
from models.fuzzcontext import FuzzMode
from eventstore import EventStore

class ServiceManager:
    
    def __init__(self, eventstore: EventStore) -> None:      
        self.eventstore = eventstore
    
        
    def discover_openapi3_by_filepath(self,
                            hostname,
                            port,
                            filePath,
                            name='',
                            fuzzMode= 'Quick',
                            numberOfFuzzcaseToExec=50,
                            isAnonymous=True,
                            basicUsername='',
                            basicPassword='',
                            bearerTokenHeader='',
                            bearerToken='',
                            apikeyHeader='',
                            apikey=''):
        
        openapi3Dis = OpenApi3ApiDiscover(self.eventstore)
        apicontext = openapi3Dis.load_openapi3_file(filePath)
        
        fcc = OpenApi3FuzzContextCreator(self.eventstore)
        fcc.new_fuzzcontext(hostname=hostname,
                            port=port,
                            fuzzMode= fuzzMode,
                            numberOfFuzzcaseToExec=numberOfFuzzcaseToExec,
                            isAnonymous=isAnonymous,
                            basicUsername=basicUsername,
                            basicPassword=basicPassword,
                            bearerTokenHeader=bearerTokenHeader,
                            bearerToken=bearerToken,
                            apikeyHeader=apikeyHeader,
                            apikey=apikey,
                            filePath=filePath)
        
        fuzzcontext = fcc.create_fuzzcontext(apicontext)
        
        return fuzzcontext
        

    