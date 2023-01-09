import os,sys
from pathlib import Path
import shortuuid
from datetime import datetime
import jinja2
from urllib.parse import urlparse
import json
from urllib.parse import urlparse

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
        self.verbs = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
        

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
            ok, error, fcSets = self.parse_request_msg_as_fuzzcasesets(requestTextContent)
        
            if not ok or len(fcSets) == 0:
                return False, error, ApiFuzzContext()
            
            fuzzcontext = ApiFuzzContext()
            fuzzcontext.Id = shortuuid.uuid()
            if name == '':
                fuzzcontext.name = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            else:
                fuzzcontext.name = name
                
            fuzzcontext.datetime = datetime.now()
            fuzzcontext.apiDiscoveryMethod = apiDiscoveryMethod
            fuzzcontext.requestTextContent = requestTextContent
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
        
        
    def parse_request_msg_as_fuzzcasesets(self, rqMsg: str) -> tuple([bool, str, list[ApiFuzzCaseSet]]):


        if rqMsg == '' or rqMsg.strip() == '':
            return []
        
        # multiline split
        
        fcSets = []
        
        rqMsgWithoutComments = self.remove_all_comments(rqMsg)
        
        # split request-blocks by delimiter ###
        multiReqMsgBlocks = rqMsgWithoutComments.strip().split('###')
        
        # each block is a fuzzcaseset
        for eachReqBlock in multiReqMsgBlocks:
            
            if eachReqBlock == '':
                continue
            
            # in 1 req message block, split it multi-line
            multilineBlock: list[str] = eachReqBlock.strip().splitlines()
            
            if len(multilineBlock) == 0:
                return True, '', fcSets  

            # remove all breaklines until first char is found
            multilineBlock = self.remove_breaklines_until_char_detected(multilineBlock)
            
            if len(multilineBlock) == 0:
                return False, 'Request Message contains no fuzz case sets', []
            
            # start request-message parsing
            fuzzcaseSet = ApiFuzzCaseSet()
            fuzzcaseSet.Id = shortuuid.uuid()
            
            # get request line: which includes VERB + (URL + querystring) + http-version (HTTP/1.1)
            
            # verb
            fuzzcaseSet.verb = self.get_verb(multilineBlock)
            
            # path
            ok, error, path, hostname, port = self.get_hostname_path(multilineBlock)
            if not ok:
                # cannot find path, skip to next block
                self.eventstore.emitErr(error)
                continue
            
            fuzzcaseSet.hostname = hostname
            fuzzcaseSet.port = port
            fuzzcaseSet.path = path
            
            pathOK, pathErr, evalPath = self.inject_eval_into_wordlist_expression(path)
            
            if not pathOK:
                return pathOK, f'Path parsing error: {Utils.errAsText(pathErr)}', []
            
            fuzzcaseSet.pathDataTemplate = evalPath
            
            # get querystring
            # lineIndex is the index of the multiline list when querystring ends at
            # multilineBlock lst will pop lines until lineIndex so that get headers will process at header line
            lineIndex, qs = self.get_querystring(multilineBlock)
            fuzzcaseSet.querystringNonTemplate = qs
            
            qsOK, qsErr, evalQS = self.inject_eval_into_wordlist_expression(qs)
            if not qsOK:
                return qsOK, f'Querystring parsing error: {Utils.errAsText(qsErr)}', []
            
            fuzzcaseSet.querystringDataTemplate = evalQS
            
            #remove requestline lines including multi-line querystring and breaklines between requestline and headers
            self.removeProcessedLines(lineIndex, multilineBlock)
                
            # get headers
            if len(multilineBlock) > 0:
                lineIndex, headers = self.get_headers(multilineBlock)
                
                headerJson = '' if len(headers) == 0 else json.dumps(headers)
                
                fuzzcaseSet.headerNonTemplate = headerJson
                
                if len(headers) > 0:
                    evalHeaderDict = {}
                    for key in headers.keys():
                        hVal = headers[key]
                        hOK, hErr, evalHeader = self.inject_eval_into_wordlist_expression(hVal)
                        if not hOK:
                            return hOK, f'Header parsing error: {Utils.errAsText(hErr)}', []
                        
                        evalHeaderDict[key] = evalHeader

                    if len(evalHeaderDict) > 0:
                        fuzzcaseSet.headerDataTemplate = '' if len(evalHeaderDict) == 0 else json.dumps(evalHeaderDict)
            
                self.removeProcessedLines(lineIndex, multilineBlock)
            
            # get body
            if len(multilineBlock) > 0:
                
                body, files = self.get_body_and_files(multilineBlock)
                
                fuzzcaseSet.bodyNonTemplate = body
                
                bOK, bErr, evalBody = self.inject_eval_into_wordlist_expression(body)
                if not bOK:
                    return bOK, f'Body parsing error: {Utils.errAsText(bErr)}', []
                
                fuzzcaseSet.bodyDataTemplate = evalBody
                
                fuzzcaseSet.file = files
                
            fcSets.append(fuzzcaseSet)
            
        return True, '', fcSets                
    
    
    def get_hostname_path(self, multilineBlock) -> tuple([bool, str, str, str, int]):
        
        path = ''
        
        if len(multilineBlock) >= 1:
            
            requestLine: str = multilineBlock[0]
            
            # remove verb
            requestLine = self.remove_verb_if_exist(requestLine)
            
            # remove HTTP/1.1 if any
            requestLine = requestLine.replace('HTTP/1.1', '')
            
            urlonly = requestLine.strip()
            
            parseOutput = urlparse(urlonly)
            
            # determine port
            port = -1
            
            scheme = parseOutput.scheme
            if parseOutput.port != None:
                port = parseOutput.port
            elif scheme.lower() == 'http':
                port = 80
            elif scheme.lower() == 'https':
                port = 443
            
            hostname = f'{parseOutput.scheme}://{parseOutput.hostname}'
            
            path = parseOutput.path.strip()
            
            return True, '', path, hostname, port
                
        return True, '', path, '', -1
    
    
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
        
        requestline = self.remove_verb_if_exist(requestline)
        
        # remove HTTP/1.1 if any
        requestline = requestline.replace('HTTP/1.1', '')
        
        requestline = requestline.strip()
        
        
        querystring = urlparse(requestline).query
        
        qsParts = querystring.split('&')
        
        qsParts = [x.strip() for x in qsParts]   # remove all prefix/suffix spaces if any
        
        querystring = '&'.join(qsParts)

        lineIndex = 0
        while self.is_next_line_querystring(multilineBlock, lineIndex, qsTokens):
            lineIndex = lineIndex + 1
        
        #lineIndex = 0
        # # claim empty breaklines in case there are between requestline and headers/body
        # while self.is_next_line_breakline(multilineBlock, lineIndex):
        #     lineIndex = lineIndex + 1
            
        mergedQSTokens = "".join(qsTokens)
        querystring = querystring + mergedQSTokens
        
        if querystring != '' and not querystring.startswith('?'):
            querystring = '?' + querystring
        
        return lineIndex, querystring
    
    def is_next_line_querystring(self, lines, lineIndex, qsTokens: list[str]):
        
        linesLen = len(lines) - 1
        nextLineIdx = lineIndex + 1
        
        if(nextLineIdx <= linesLen):
            
            qsline = lines[nextLineIdx].strip()
            
            if(Utils.isCharsInString(['?', '&'], qsline)):
                qsTokens.append(qsline)
                return True
            else:
                return False
        
        return False

    
    def get_verb(self, multilineBlock: list[str]) -> tuple([bool, str, str]):
        
        
        verb = 'GET'
        
        if len(multilineBlock) >= 1:
            requestline = multilineBlock[0]
            
            tokens = requestline.split(' ')
            
            if len(tokens) >= 1:
                
                t = tokens[0]
                
                for v in self.verbs:
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
            
            # breakline marker that divides header and body
            if line == '':
                return lineIndex, headers
            
            #ignore invalid header format
            if not self.is_header(line):
                lineIndex = lineIndex + 1
                continue                
            
            lineIndex = lineIndex + 1
            
            if Utils.isInString(':', line):
                
                sh = line.split(':')
                
                if len(sh) != 2:
                    continue
                
                headerKey = sh[0].strip()
                headerVal = sh[1].strip()
                
                if headerKey == '' or headerVal == '':
                    continue
                
                headers[headerKey] = headerVal
                

        # minus 1 to cater for zero-index in list
        if lineIndex > 0:
            lineIndex = lineIndex - 1
            
        return lineIndex, headers
    
    def is_header(self, line: str) -> bool:
        
        if line.strip() == '':
            return False
        
        if Utils.isInString(':', line):
            
            splitted = line.split(':')
            
            if len(splitted) != 2:
                return False
            
            key = splitted[0]
            val = splitted[1]
            
            if key == '' or val == '':
                return False
            
            return True
            
        return False
    
    def remove_verb_if_exist(self, requestline: str):
            if requestline == '':
                return requestline
            for v in self.verbs:
                if requestline.upper().startswith(v):
                    requestline = requestline.removeprefix(v)
            return requestline
    
    #example:
    # POST https://api.example.com/login HTTP/1.1
    # Content-Type: application/x-www-form-urlencoded

    # name=foo
    # &password=bar
    def get_body_and_files(self, multilineBlock: list[str]) -> str:
        
        body = []
        files = []
        
        for line in multilineBlock:
            
            line = line.strip()
            
            # breakline marker for multipart/form-data
            if line == '':
                continue
            
            yes, exprType = Utils.is_file_wordlist_type(line)
            
            if yes:
                files.append(exprType)
                continue
        
            body.append(line)
            
        
        return ''.join(body), files
            
    
    def removeProcessedLines(self, toIndex, list):
        
        if toIndex == 0:
            del list[0]
            return
        
        idx = 0
         
        while idx <= toIndex :
            del list[0]
            idx = idx + 1
            
    # a comment is consider # or //  
    # a request-block delimiter is '###', so a special check is needed to avoid conflict with comment (#)  
    def is_line_comment(self, line: str):
        
        # checks if its a delimiter for a request-block
        # blockdelimiter = re.match('\B###', line)
        # if blockdelimiter is not None and len(blockdelimiter.regs) > 0:
        #     return False
        
        line = line.strip()
        
        if line.startswith('//'):
            return True
        
        if '###' in line:
            return False
        
        line = line.strip()
        if line.startswith('#'):
            return True
        
        return False
    
    
    def remove_breaklines_until_char_detected(self, lines: list[str]) -> list[str]:
        for l in lines:
            
            ls = l.strip()
            
            if ls != '':
                return lines
            
            if ls == '':
                lines.remove(l)
                
        return lines
    
    
    def remove_all_comments(self, rqMsg: str) -> str: 
        
        lines = rqMsg.splitlines()
        lines = [x for x in lines if not self.is_line_comment(x)]
        return '\n'.join(lines)
    
    
    # integer type is to support OpenApi3, but is same as digit
    def jinja_wordlist_types_render_dict(self) -> dict:
        return {
            'string': '{{ eval(wordlist_type=\'string\') }}',
            'bool':  '{{ eval(wordlist_type=\'bool\') }}',
            'digit': '{{ eval(wordlist_type=\'digit\') }}',
            'integer': '{{ eval(wordlist_type=\'integer\') }}',
            'char': '{{ eval(wordlist_type=\'char\') }}',
            'filename': '{{ eval(wordlist_type=\'filename\') }}',
            'datetime': '{{ eval(wordlist_type=\'datetime\') }}',
            'date': '{{ eval(wordlist_type=\'date\') }}',
            'time': '{{ eval(wordlist_type=\'time\') }}',
            'username': '{{ eval(wordlist_type=\'username\') }}',
            'password': '{{ eval(wordlist_type=\'password\') }}'
        }
        
    # insert eval into wordlist expressions e.g: {{ string }} to {{ eval(string) }}
    # this is for corpora_context to execute eval function to build up the corpora_context base on wordlist-type
    def inject_eval_into_wordlist_expression(self, expr: str) -> tuple([bool, str, str]):
        
        try:
            
        
            jinja2.filters.FILTERS['my'] = self.wordlisttype_filter_my
            
            jinja2.filters.FILTERS['myfile'] = self.wordlisttype_filter_filecontent

            tpl = jinja2.Template(expr)
            
            output = tpl.render(self.jinja_wordlist_types_render_dict())
            # output = tpl.render(
            #     string='{{ eval(wordlist_type=\'string\') }}',
            #     bool='{{ eval(wordlist_type=\'bool\') }}',
            #     digit='{{ eval(wordlist_type=\'digit\') }}',
            #     integer='{{ eval(wordlist_type=\'integer\') }}',
            #     char='{{ eval(wordlist_type=\'char\') }}',
            #     filename='{{ eval(wordlist_type=\'filename\') }}',
            #     datetime='{{ eval(wordlist_type=\'datetime\') }}',
            #     date='{{ eval(wordlist_type=\'date\') }}',
            #     time='{{ eval(wordlist_type=\'time\') }}',
            #     username='{{ eval(wordlist_type=\'username\') }}',
            #     password='{{ eval(wordlist_type=\'password\') }}'
            # )                   
                    
            return True, '', output
        
        except Exception as e:
            return False, e,  expr
        
    # insert my wordlist type
    def wordlisttype_filter_my(self, value, my_uniquename = ''):
        return f'{{{{ eval(wordlist_type=\'my\', my_value=\'{value}\', my_uniquename=\'{my_uniquename}\') }}}}'
    
    def wordlisttype_filter_filecontent(self, content, filename):
        
        output = self.render_standard_wordlist_types(content)
        
        return f'{{{{ eval(wordlist_type=my_file_content, my_file_content_value=\'{output}\', my_file_content_filename=\'{filename}\') }}}}'
    
    
    def render_standard_wordlist_types(self, expr):
        
        tpl = jinja2.Template(expr)
        
        output = tpl.render(self.jinja_wordlist_types_render_dict())  
        # output = tpl.render(
        #     string='{{ eval(wordlist_type=\'string\') }}',
        #     bool='{{ eval(wordlist_type=\'bool\') }}',
        #     digit='{{ eval(wordlist_type=\'digit\') }}',
        #     integer='{{ eval(wordlist_type=\'integer\') }}',
        #     char='{{ eval(wordlist_type=\'char\') }}',
        #     filename='{{ eval(wordlist_type=\'filename\') }}',
        #     datetime='{{ eval(wordlist_type=\'datetime\') }}',
        #     date='{{ eval(wordlist_type=\'date\') }}',
        #     time='{{ eval(wordlist_type=\'time\') }}',
        #     username='{{ eval(wordlist_type=\'username\') }}',
        #     password='{{ eval(wordlist_type=\'password\') }}'
        # )
        
        return output
    
    

        
        
            
        
                
        
            
            
        
        
        
        
        
    