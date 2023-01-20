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

import jsonpickle 
from utils import Utils
from webapi_fuzzcontext import (ApiFuzzCaseSet, ApiFuzzContext, FuzzCaseSetFile, WordlistType)
from eventstore import EventStore
from jinja2 import Environment
    
class RequestMessageFuzzContextCreator:

    
    def __init__(self):
        self.apicontext = None
        self.fuzzcontext = ApiFuzzContext()
        self.eventstore = EventStore()
        self.verbs = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
        
        # currentFuzzCaseSet:
        # use for jinja filters to access current processing fuzzcaseset
        # for now, used by only myfile filter
        self.currentFuzzCaseSet = None
        
        self.env = jinja2.Environment()
        self.env.filters[WordlistType.my] = self.my_jinja_filter
        self.env.filters[WordlistType.myfile] = self.myfile_jinja_filter

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
            
    def parse_first_request_msg_as_single_fuzzcaseset(self, rqMsg: str) -> tuple([bool, str, ApiFuzzCaseSet]):
        
        if rqMsg == '' or rqMsg.strip() == '':
            return True, '', []
        
        rqMsgWithoutComments = self.remove_all_comments(rqMsg)
        
        splittedRqBlocks = rqMsgWithoutComments.strip().split('###')
        
        singleRQBlock = ''
        
        if len(splittedRqBlocks) > 0:
            singleRQBlock = splittedRqBlocks[0]
        
        if singleRQBlock == '' or singleRQBlock.strip() == '':
            return True, '', []
        
        ok, error, fcsList = self.parse_request_msg_as_fuzzcasesets(singleRQBlock)
        
        fcsSingleResult = None
        if ok and len(fcsList) > 0:
            fcsResult = fcsList[0]
            
        return True, '', fcsResult
        
    # parse_request_msg_as_fuzzcasesets
    # take means process the number of request-msg-blocks within the entire Request MEssage.
    # # -1 means take-in all
    def parse_request_msg_as_fuzzcasesets(self, rqMsg: str) -> tuple([bool, str, list[ApiFuzzCaseSet]]):


        if rqMsg == '' or rqMsg.strip() == '':
            return True, '', []
        
        # multiline split
        
        fcSets = []
        
        rqMsgWithoutComments = self.remove_all_comments(rqMsg)
        
        # split request-blocks by delimiter ###
        requestBlocks = rqMsgWithoutComments.strip().split('###')
        
        # each block is a fuzzcaseset
        for eachReqBlock in requestBlocks:
            
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
            self.currentFuzzCaseSet = fuzzcaseSet
            self.currentFuzzCaseSet.requestMessage = eachReqBlock
            
            # get request line: which includes VERB + (URL + querystring) + http-version (HTTP/1.1)
            
            # verb
            self.currentFuzzCaseSet.verb = self.get_verb(multilineBlock)
            
            # path
            ok, error, path, hostname, port = self.get_hostname_path(multilineBlock)
            if not ok:
                # cannot find path, skip to next block
                self.eventstore.emitErr(error)
                continue
            
            self.currentFuzzCaseSet.hostname = hostname
            self.currentFuzzCaseSet.port = port
            self.currentFuzzCaseSet.path = path
            
            pathOK, pathErr, evalPath = self.inject_eval_into_wordlist_expression(path)
            
            if not pathOK:
                return pathOK, f'Path parsing error: {Utils.errAsText(pathErr)}', []
            
            self.currentFuzzCaseSet.pathDataTemplate = evalPath
            
            # get querystring
            # lineIndex is the index of the multiline list when querystring ends at
            # multilineBlock lst will pop lines until lineIndex so that get headers will process at header line
            lineIndex, qs = self.get_querystring(multilineBlock)
            self.currentFuzzCaseSet.querystringNonTemplate = qs
            
            qsOK, qsErr, evalQS = self.inject_eval_into_wordlist_expression(qs)
            if not qsOK:
                return qsOK, f'Querystring parsing error: {Utils.errAsText(qsErr)}', []
            
            self.currentFuzzCaseSet.querystringDataTemplate = evalQS
            
            #remove requestline lines including multi-line querystring and breaklines between requestline and headers
            self.removeProcessedLines(lineIndex, multilineBlock)
                
            # get headers
            if len(multilineBlock) > 0:
                lineIndex, headers = self.get_headers(multilineBlock)
                
                headerJson = '' if len(headers) == 0 else json.dumps(headers)
                
                self.currentFuzzCaseSet.headerNonTemplate = headerJson
                
                if len(headers) > 0:
                    evalHeaderDict = {}
                    for key in headers.keys():
                        hVal = headers[key]
                        hOK, hErr, evalHeader = self.inject_eval_into_wordlist_expression(hVal)
                        if not hOK:
                            return hOK, f'Header parsing error: {Utils.errAsText(hErr)}', []
                        
                        evalHeaderDict[key] = evalHeader

                    if len(evalHeaderDict) > 0:
                        self.currentFuzzCaseSet.headerDataTemplate = '' if len(evalHeaderDict) == 0 else json.dumps(evalHeaderDict)
            
                self.removeProcessedLines(lineIndex, multilineBlock)
            
            # get body
            if len(multilineBlock) > 0:
                
                fileExpr, fileType  =self.get_file_type_in_body(multilineBlock)
                
                # myfile will be discovered later in "inject_eval_into_wordlist_expression"
                body = self.get_body_as_str(multilineBlock)
                
                myfile = self.parse_myfile_in_body_if_any(body)
                
                if myfile != '':
                    self.currentFuzzCaseSet.file = myfile
                    self.currentFuzzCaseSet.fileDataTemplate = myfile.content
                else:
                    # check if body contains file, pdf, image wordlist type
                    if fileExpr != '' and fileType != '':
                        fOK, fErr, evalFile = self.inject_eval_into_wordlist_expression(fileExpr)
                        if not fOK:
                            return fOK, f'File parsing error: {Utils.errAsText(fErr)}', []
                        
                        self.currentFuzzCaseSet.file = FuzzCaseSetFile(wordlist_type=fileType, filename=fileType)
                        self.currentFuzzCaseSet.fileDataTemplate = evalFile
                    
                    # body has content
                    else:
                        bbOK, bErr, evalBody = self.inject_eval_into_wordlist_expression(body)
                        if not bbOK:
                            return bbOK, f'Body parsing error: {Utils.errAsText(bErr)}', []
                        
                        self.currentFuzzCaseSet.bodyDataTemplate = evalBody
                        self.currentFuzzCaseSet.bodyNonTemplate = body
                
                
                
                # currently, fuzzie only supports 1 file upload per request block.
                # When there is 1 file detected, this file takes up whole request body.
                # which means for multipart-form, fuzzie uploads only a single file's content and not mix file and other data types together
                # check for myfile wordlist type
                # elif isinstance(self.currentFuzzCaseSet.file, FuzzCaseSetFile) and self.currentFuzzCaseSet.file.wordlist_type == WordlistType.myfile:
                #     self.currentFuzzCaseSet.bodyNonTemplate = ''
                #     self.currentFuzzCaseSet.bodyDataTemplate = ''  # myfile uses body can file content
                #     self.currentFuzzCaseSet.fileDataTemplate = evalBody                    
                   

            fcSets.append(self.currentFuzzCaseSet)
            
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
    def get_body_as_str(self, multilineBlock: list[str]) -> str:
        
        body = ''
        copiedMB = []
        
        # check lines for file wordlist type
        for line in multilineBlock:
            
            line = line.strip()
            
            # breakline marker for multipart/form-data
            if line == '':
                copiedMB.append(line)
                continue
            
            # check if body contains {{file}}, {{image}} or {{pdf}}
            yes, _ = Utils.is_file_wordlist_type(line)
            
            if yes:
                continue
            else:
                copiedMB.append(line)   # append lines without {{file}}, {{image}} or {{pdf}}
        
        # get body in original string as a whole including all whitespaces and breaklines
        for s in copiedMB:
            body = body + s + '\n'
        
        return body
    
    def get_file_type_in_body(self,  multilineBlock: list[str]):
        
        fileExpr = ''
        fileType = ''
        
        # check lines for file wordlist type
        for line in multilineBlock:
            
            line = line.strip()
            
            # breakline marker for multipart/form-data
            if line == '':
                continue
            
            # check if body contains {{file}}, {{image}} or {{pdf}}
            yes, fType = Utils.is_file_wordlist_type(line)
            
            if yes:
                fileExpr = line         # line will contain the curly braces e.g {{ file }}
                fileType = fType
        
        return fileExpr, fileType
    
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
    def jinja_primitive_wordlist_types_render_dict(self) -> dict:
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
            'password': '{{ eval(wordlist_type=\'password\') }}',
            'image': '{{ eval(wordlist_type=\'image\') }}',
            'pdf': '{{ eval(wordlist_type=\'pdf\') }}',
            'file': '{{ eval(wordlist_type=\'file\') }}',
        }
        
    # insert eval into wordlist expressions e.g: {{ string }} to {{ eval(string) }}
    # this is for corpora_context to execute eval function to build up the corpora_context base on wordlist-type
    def inject_eval_into_wordlist_expression(self, expr: str) -> tuple([bool, str, str]):
        
        try:
        
            tpl = self.env.from_string(expr)
            
            output = tpl.render(self.jinja_primitive_wordlist_types_render_dict())                
                    
            return True, '', output
        
        except Exception as e:
            return False, e,  expr
        
    # insert my wordlist type
    def my_jinja_filter(self,value, my_uniquename = ''):
        
        # escape single quote if any
        output = output.replace("'", "\\'")
        
        evalOutput = f'{{{{ eval(wordlist_type=\'{WordlistType.my}\', my_value=\'{value}\', my_uniquename=\'{my_uniquename}\') }}}}'
        
        #escape single quotes if any
        evalOutput = evalOutput.replace("'", "\\'")
        
        return evalOutput
    
    def parse_myfile_in_body_if_any(self, body) -> FuzzCaseSetFile:
        
        fileResult = '';
        
        tpl = self.env.from_string(body)
        
        output = tpl.render()
        
        if output != '':
            jsonDecoded = jsonpickle.decode(output)
            if isinstance(jsonDecoded, FuzzCaseSetFile):
                fileResult = jsonpickle.decode(output)
        
        return fileResult
            
    
    def myfile_jinja_filter(self, content: str, filename: str):
        
        output = self.render_standard_wordlist_types(content)
        
        evalOutput =  f'{{{{ eval(wordlist_type="{WordlistType.myfile}", my_file_content_value="{output}", my_file_content_filename="{filename}") }}}}'
        
        # used in corpora_context to find myfile_corpora to supply myfile data
        corporaContextKeyName = f'{WordlistType.myfile}_{filename}'
        
        # *create file object in current fuzzcaseset
        if self.currentFuzzCaseSet != None:
           self.currentFuzzCaseSet.file = FuzzCaseSetFile(
                   wordlist_type=corporaContextKeyName, #WordlistType.myfile,
                   filename = corporaContextKeyName,
                   content=evalOutput)
        
        return jsonpickle.encode(
            FuzzCaseSetFile(
                   wordlist_type=corporaContextKeyName, #WordlistType.myfile,
                   filename = corporaContextKeyName,
                   content=evalOutput)
                                 )
    
    
    def render_standard_wordlist_types(self, expr):
        
        tpl = jinja2.Template(expr)
        
        output = tpl.render(self.jinja_primitive_wordlist_types_render_dict())  

        return output
    
    

        
        
            
        
                
        
            
            
        
        
        
        
        
    