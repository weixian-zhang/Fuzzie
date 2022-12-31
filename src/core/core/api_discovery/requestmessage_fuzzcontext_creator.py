import os,sys
from pathlib import Path
import shortuuid
from datetime import datetime
import base64
from urllib.parse import urlparse
import json

parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from utils import Utils
from webapi_fuzzcontext import ApiFuzzCaseSet, ApiFuzzContext
from eventstore import EventStore

class RequestMessageFuzzContextCreator:
    
    def __init__(self):
        self.apicontext = None
        self.fuzzcontext = ApiFuzzContext()
        self.eventstore = EventStore()
        

    def new_fuzzcontext(self,
                 apiDiscoveryMethod,  
                 hostname, 
                 port,
                 authnType,
                 name = '',
                 requestTextContent = '',
                 requestTextFilePath = '',
                 openapi3FilePath = '',
                 openapi3Url = '',
                 openapi3Content = '',
                 fuzzcaseToExec = 100,
                 basicUsername = '',
                 basicPassword = '',
                 bearerTokenHeader = '',
                 bearerToken = '',
                 apikeyHeader = '',
                 apikey = '') -> tuple([bool, str, ApiFuzzContext]):
        
        try:
            ok, error, fcSets = self.parse_req_msg_into_fuzzcasesets(requestTextContent)
        
            if not ok or len(fcSets) == 0:
                return False, 'request message is empty, no context is created', ApiFuzzContext()
            
            fuzzcontext = ApiFuzzContext()
            fuzzcontext.Id = shortuuid.uuid()
            if name == '':
                fuzzcontext.name = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            else:
                fuzzcontext.name = name
                
            fuzzcontext.datetime = datetime.now()
            fuzzcontext.apiDiscoveryMethod = apiDiscoveryMethod
            fuzzcontext.requestMessageText = requestTextContent
            fuzzcontext.requestMessageFilePath = requestTextFilePath
            fuzzcontext.openapi3FilePath = openapi3FilePath
            fuzzcontext.openapi3Content = openapi3Content
            fuzzcontext.openapi3Url = openapi3Url
            fuzzcontext.hostname = hostname
            fuzzcontext.port = port
            fuzzcontext.authnType = authnType
            fuzzcontext.fuzzcaseToExec = fuzzcaseToExec
            
            fuzzcontext.basicUsername = basicUsername
            fuzzcontext.basicPassword= basicPassword
            fuzzcontext.bearerTokenHeader= bearerTokenHeader
            fuzzcontext.bearerToken= bearerToken 
            fuzzcontext.apikeyHeader=  apikeyHeader 
            fuzzcontext.apikey= apikey
            
            fuzzcontext.fuzzcaseSets = fcSets
            
            return True, '', fuzzcontext
        except Exception as e:
            self.eventstore.emitErr(e)
        
        
    def parse_req_msg_into_fuzzcasesets(self, rqMsgBase64: str) -> tuple([bool, str, list[ApiFuzzCaseSet]]):

        rqMsg = base64.b64decode(rqMsgBase64).decode('UTF-8')

        if rqMsg == '' or rqMsg.strip() == '':
            return []
        
        # multiline split
        
        fcSets = []
        
        multiReqMsgBlocks = rqMsg.strip().split('###')
        
        # each block is a fuzzcaseset
        for eachReqBlock in multiReqMsgBlocks:
            
            # in 1 req message block, split it multi-line
            multilineBlock: list[str] = eachReqBlock.strip().splitlines()
            
            if len(multilineBlock) == 0:
                return 
            
            fuzzcaseSet = ApiFuzzCaseSet()
            fuzzcaseSet.Id = shortuuid.uuid()
            
            # get request line: which includes VERB + (URL + querystring) + http-version (HTTP/1.1)
            
    
            # verb
            fuzzcaseSet.verb = self.get_verb(multilineBlock)
            
            # path
            ok, error, path = self.get_path(multilineBlock)
            
            if not ok:
                # cannot find path, skip to next block
                self.eventstore.emitErr(error)
                continue
            
            fuzzcaseSet.path = path
            fuzzcaseSet.pathDataTemplate = path
            
            # get querystring
            # lineIndex is the index of the multiline list when querystring ends at
            # multilineBlock lst will pop lines until lineIndex so that get headers will process at header line
            lineIndex, qs = self.get_querystring(multilineBlock)
            fuzzcaseSet.querystringNonTemplate = qs
            fuzzcaseSet.querystringDataTemplate = qs
            
            #remove requestline lines including multi-line querystring
            self.popItemsInList(lineIndex, multilineBlock)
            # for idx in range(0, lineIndex):
            #     del multilineBlock[idx]
                
            # get headers
            lineIndex, headers = self.get_headers(multilineBlock)
            fuzzcaseSet.headerNonTemplate = json.dumps(headers)
            fuzzcaseSet.headerDataTemplate = headers
            
            self.popItemsInList(lineIndex, multilineBlock)
            
            # get body
                
                
            fcSets.append(fuzzcaseSet)
            
        return True, '', fcSets
        
        # fuzzcaseSet.Id = shortuuid.uuid()
        #     fuzzcaseSet.verb = api.verb.name
            
        #     fuzzcaseSet.path = api.path
            
        #     fuzzcaseSet.pathDataTemplate= self.create_path_data_template(api)
            
        #     querystring = self.create_querystring_data_template(api)
        #     fuzzcaseSet.querystringDataTemplate = querystring
        #     fuzzcaseSet.querystringNonTemplate = self.remove_micro_template_for_gui_display(querystring)
            
        #     body = self.create_body_data_template(api)
        #     fuzzcaseSet.bodyDataTemplate = body
        #     fuzzcaseSet.bodyNonTemplate = self.remove_micro_template_for_gui_display(json.dumps(body))
            
        #     header = self.create_header_data_template(api)
        #     fuzzcaseSet.headerDataTemplate = header
        #     fuzzcaseSet.headerNonTemplate =  self.remove_micro_template_for_gui_display(json.dumps(header))
    
    # def process_request_line(self, requestline: str, fuzzcaseSet: ApiFuzzCaseSet) -> tuple([bool, str]):
        
    #     multilineBlock = requestline.strip().splitlines()
        
    #     # verb
    #     fuzzcaseSet.verb = self.get_verb(multilineBlock)
        
    #     #path
    #     path = self.get_path(multilineBlock)
    #     fuzzcaseSet.path = path
    #     fuzzcaseSet.pathDataTemplate = path
        
    #     #querystring
        
        
                
                
    def get_path(self, multilineBlock) -> tuple([bool, str, str]):
        
        path = ''
        
        if len(multilineBlock) >= 1:
            
            requestLine = multilineBlock[0]
            
            tokens = requestLine.split(' ')
            
            for idx, t in enumerate(tokens):
                
                if Utils.validUrl(t) == False:
                    continue
                
                path = urlparse(t).path
                return True, '', path
        
        if path == '':
            return False, 'request line contains invalid URL', path
                
        return True, '', path
        
    
     # examples
     # GET https://example.com/comments?page=2
        # &pageSize=10
     #or
     # GET https://example.com/comments
        # ?page=2
        # &pageSize=10
        
    def get_querystring(self, multilineBlock) -> tuple([int, str]):
        
        qsChars = ['?', '&']
        qsTokens = []
        querystring = ''
        
        # search for singleline multistring
        
        requestline = multilineBlock[0]
        
        tokens = requestline.split(' ')
        
        try:
            for t in tokens:
                t = t.strip()
                if Utils.isInString('?', t):
                    querystring = urlparse(t).query
                    querystring = '?' + querystring
                    break
        except ValueError as e:
            #substring not found exception
            pass
           

        lineIndex = 0
        while self.is_next_line_querystring(multilineBlock, lineIndex, qsChars, qsTokens):
            lineIndex = lineIndex + 1
            
        mergedQSTokens = "".join(qsTokens)
        querystring = querystring + mergedQSTokens
        
        return lineIndex, querystring
    
    def is_next_line_querystring(self, lines, lineIndex, qsChars, qsTokens: list[str]):
        
        linesLen = len(lines) - 1
        nextLineIdx = lineIndex + 1
        
        if(nextLineIdx <= linesLen):
            
            qsline = lines[nextLineIdx].strip()
            
            if(Utils.isCharsInString(qsChars, qsline)):
                qsTokens.append(qsline)
                return True
            else:
                return False
        
        return False
    
    def get_verb(self, multilineBlock: list[str]) -> tuple([bool, str, str]):
        
        verbs = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
        verb = 'GET'
        
        if len(multilineBlock) >= 1:
            requestline = multilineBlock[0]
            
            tokens = requestline.split(' ')
            
            if len(tokens) >= 1:
                
                t = tokens[0]
                
                for v in verbs:
                    if v == t:
                        verb = v
                        return verb
        
        return verb
    
    
    # parse the follow example
    # User-Agent: rest-client
    # Accept-Language: en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4
    # Content-Type: application/json
    def get_headers(self, multilineBlock: list[str]) -> tuple([int, dict]):
        
        lineIndex = 0
        headers = {}
        
        for line in multilineBlock:
            line = line.strip()
            if Utils.isInString(':', line):
                
                sh = line.split(':')
                
                if len(sh) != 2:
                    continue
                
                headerKey = sh[0]
                headerVal = sh[1]
                
                headers[headerKey] = headerVal
                
            lineIndex = lineIndex + 1
        
        # minus 1 to cater for zero-index in list
        if lineIndex > 0:
            lineIndex = lineIndex - 1
            
        return lineIndex, headers
    
    
    def popItemsInList(self, toIndex, list):
        
        if toIndex == 0:
            del list[0]
            return
        
        idx = 0
         
        while idx <= toIndex :
            del list[0]
            idx = idx + 1
                
        
            
            
        
        
        
        
        
    