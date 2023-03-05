import os,sys
from pathlib import Path
import shortuuid
from datetime import datetime
from urllib.parse import urlparse
import json
from urllib.parse import urlparse

from api_discovery.wordlist_type_helper import WordlistTypeHelper

parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

import re
import validators
from utils import Utils
from webapi_fuzzcontext import (ApiFuzzCaseSet, ApiFuzzContext, FuzzCaseSetFile, WordlistType)
from eventstore import EventStore

    
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
        
        # self.jinjaEnvPrimitive = jinja2.Environment()
        # self.jinjaEnvPrimitive.filters[WordlistType.mutate] = self.mutate_jinja_filter
        
        self.jinjaEnvPrimitive  = WordlistTypeHelper.create_jinja_primitive_env(
            mutate_jinja_filter=self.mutate_jinja_filter,
            jinja_numrange_func=self.jinja_numrange_func)
        
        self.jinjaEnvBody = WordlistTypeHelper.create_jinja_body_env(mutate_jinja_filter=self.mutate_jinja_filter,
                                                                     myfile_jinja_filter=self.myfile_jinja_filter,
                                                                     jinja_file_func=self.jinja_file_func,
                                                                     jinja_image_func=self.jinja_image_func,
                                                                     jinja_pdf_func=self.jinja_pdf_func,
                                                                     jinja_numrange_func=self.jinja_numrange_func)
        
        # self.jinjaEnvBody = jinja2.Environment()
        # self.jinjaEnvBody.filters[WordlistType.mutate] = self.mutate_jinja_filter
        # self.jinjaEnvBody.filters[WordlistType.myfile] = self.myfile_jinja_filter
        # self.jinjaEnvBody.globals['image'] = self.jinja_image_func
        # self.jinjaEnvBody.globals['file'] = self.jinja_file_func
        # self.jinjaEnvBody.globals['pdf'] = self.jinja_pdf_func
        

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
            
            # parse verb
            self.currentFuzzCaseSet.verb = self.get_verb(multilineBlock)
            
            # parse path
            ok, error, path, hostname, port = self.get_hostname_path(multilineBlock)
            if not ok:
                # cannot find path, skip to next block
                self.eventstore.emitErr(error)
                return False, error, [] 
            
            self.currentFuzzCaseSet.hostname = hostname
            self.currentFuzzCaseSet.port = port
            self.currentFuzzCaseSet.path = path
            
            pathOK, pathErr, evalPath = self.inject_eval_func_primitive_wordlist(path)
            
            if not pathOK:
                return pathOK, f'Path parsing error: {Utils.errAsText(pathErr)}', []
            
            self.currentFuzzCaseSet.pathDataTemplate = evalPath
            
            # parse querystring
            # lineIndex is the index of the multiline list when querystring ends at
            # multilineBlock lst will pop lines until lineIndex so that get headers will process at header line
            lineIndex, qs = self.get_querystring(multilineBlock)
            self.currentFuzzCaseSet.querystringNonTemplate = qs
            
            qsOK, qsErr, evalQS = self.inject_eval_func_primitive_wordlist(qs)
            if not qsOK:
                return qsOK, f'Querystring parsing error: {Utils.errAsText(qsErr)}', []
            
            self.currentFuzzCaseSet.querystringDataTemplate = evalQS
            
            #remove requestline lines including multi-line querystring and breaklines between requestline and headers
            self.removeProcessedLines(lineIndex, multilineBlock)
                
            # parse headers
            headers = {}
            if len(multilineBlock) > 0:
                lineIndex, headers = self.get_headers(multilineBlock)
                
                headerJson = '' if len(headers) == 0 else json.dumps(headers)
                
                self.currentFuzzCaseSet.headerNonTemplate = headerJson
                
                if len(headers) > 0:
                    evalHeaderDict = {}
                    for key in headers.keys():
                        hVal = headers[key]
                        hOK, hErr, evalHeader = self.inject_eval_func_primitive_wordlist(hVal)
                        if not hOK:
                            return hOK, f'Header parsing error: {Utils.errAsText(hErr)}', []
                        
                        evalHeaderDict[key] = evalHeader

                    if len(evalHeaderDict) > 0:
                        self.currentFuzzCaseSet.headerDataTemplate = '' if len(evalHeaderDict) == 0 else json.dumps(evalHeaderDict)
            
                self.removeProcessedLines(lineIndex, multilineBlock)
            
            # parse body
            lineIndex = 0
            body = ''
            graphqlVariable = ''
            if len(multilineBlock) > 0:
                
                self.remove_breaklines_until_char_detected(multilineBlock)
                
                if self.is_grapgql(headers):
                   ok, error, body, graphqlVariable = self.graphql_get_body_and_variable(multilineBlock)
                   
                   if ok:
                        bodyTpl = self.jinjaEnvPrimitive.from_string(body)
                        bodyEval = bodyTpl.render(WordlistTypeHelper.jinja_primitive_wordlist_types_dict()) #bodyTpl.render(self.jinja_primitive_wordlist_types_dict())
                        
                        gqlVariableTpl = self.jinjaEnvPrimitive.from_string(graphqlVariable)
                        graphqlVariableEval = gqlVariableTpl.render(WordlistTypeHelper.jinja_primitive_wordlist_types_dict()) #gqlVariableTpl.render(self.jinja_primitive_wordlist_types_dict())
                        
                        self.currentFuzzCaseSet.isGraphQL = True
                        self.currentFuzzCaseSet.graphQLVariableNonTemplate = graphqlVariable
                        self.currentFuzzCaseSet.graphQLVariableDataTemplate = graphqlVariableEval
                        self.currentFuzzCaseSet.bodyNonTemplate = body
                        self.currentFuzzCaseSet.bodyDataTemplate = bodyEval
                   else:
                       return False, error, []
                else:
                    body = self.get_body_as_one_str(multilineBlock)
                
                    # jinja wil execute all filters and file-functions bind to image, pdf, file
                    tpl = self.jinjaEnvBody.from_string(body)
                    bodyRendered = tpl.render(WordlistTypeHelper.jinja_primitive_wordlist_types_dict()) #tpl.render(self.jinja_primitive_wordlist_types_dict())
                    
                    if self.is_rendered_body_has_func(bodyRendered):
                        return False, 'missing parentheses for file wordlist type. e.g: {{ image() }} {{ pdf() }} {{ file() }} {{ '' | myfile() }}', [] 

                    # no file found in body
                    if Utils.isNoneEmpty(self.currentFuzzCaseSet.file):
                        self.currentFuzzCaseSet.bodyDataTemplate = bodyRendered
                        self.currentFuzzCaseSet.bodyNonTemplate = body
                    # *has file in body containing file kind myfile, file, image or pdf
                    else:
                        if self.currentFuzzCaseSet.file == WordlistType.myfile and self.currentFuzzCaseSet.fileDataTemplate == '':
                            return False, 'error when parsing file-content myfile wordlist,', []
                            
                        self.currentFuzzCaseSet.bodyNonTemplate = ''
                        self.currentFuzzCaseSet.bodyDataTemplate = ''           

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
            
            if not validators.url(hostname):
                return False, f'Invalid hostname {hostname}', path, hostname, port
            
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
        
        querystring = '&'.join(map(str, qsParts))

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
                    if v == t.upper():
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
            
            lineIndex = lineIndex + 1
            
            if Utils.isInString(':', line):
                
                semicolonIdx = line.find(':')
                afterSemicolonIdx = semicolonIdx + 1
                
                if afterSemicolonIdx > len(line):
                    return False
                
                header = line[:semicolonIdx]
                header = header.strip()
                
                value = line[afterSemicolonIdx:]
                value = value.strip()
                
                if Utils.isNoneEmpty(header) or Utils.isNoneEmpty(value):
                    continue
                
                headers[header] = value
                

        # minus 1 to cater for zero-index in list
        if lineIndex > 0:
            lineIndex = lineIndex - 1
            
        return lineIndex, headers
    
    
    def remove_verb_if_exist(self, requestline: str):
            if requestline == '':
                return requestline
            
            rlu = requestline.upper()
            for v in self.verbs:
                if rlu.startswith(v):
                    requestline = re.sub(f'^{v}', '', requestline, count=1, flags=re.IGNORECASE)
                    requestline = requestline.strip()
                    break
            return requestline
    
    #example:
    # POST https://api.example.com/login HTTP/1.1
    # Content-Type: application/x-www-form-urlencoded

    # name=foo
    # &password=bar
    def get_body_as_one_str(self, multilineBlock: list[str]) -> str:
        
        newBody = []
        
        for line in multilineBlock:
            line = line.strip()
            newBody.append(line)
        
        return '\n'.join(newBody)

    def graphql_get_body_and_variable(self, multilineBlock: list[str]) -> tuple([str, dict]):
        
        try:
            body = []
            variable = []
            bodyStr = ''
            variableJsonStr = ''
            
            gqlVariableSeparatorIndex = 0
            for idx, line in enumerate(multilineBlock):
                line = line.strip()
                # check for empty breakline that marks "separator" between body and variable
                if line == '':
                    gqlVariableSeparatorIndex = idx
                    break
            
            # no variable block found
            if gqlVariableSeparatorIndex == 0:
                body = multilineBlock
                bodyStr = '\n'.join(body)
                
            # has variable
            else:
                body = multilineBlock[:gqlVariableSeparatorIndex]
            
                if gqlVariableSeparatorIndex + 1 <= (len(multilineBlock) - 1):
                    gqlVariableSeparatorIndex = gqlVariableSeparatorIndex + 1
                    
                variable = multilineBlock[gqlVariableSeparatorIndex:]
                
                bodyStr = '\n'.join(body)
                
                if len(variable) > 0:
                    
                    gqlVariableStr = '\n'.join(variable)
                    # variableDict =jsonpickle.decode(gqlVariableStr, safe=False)
                    # variableJsonStr = json.dumps(variableDict)
                    variableJsonStr = gqlVariableStr
                
            return True, '', bodyStr, variableJsonStr
        
        except Exception as e:
            return False, Utils.errAsText(e), '', ''
        
      
    
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
        
        lineIndex = -1
        
        for l in lines:
            
            ls = l.strip()
            
            if ls == '':
                lineIndex = lineIndex + 1
            else:
                break
            
        if lineIndex != -1:
            self.removeProcessedLines(lineIndex, lines)
                
        return lines
    
    
    def remove_all_comments(self, rqMsg: str) -> str: 
        
        lines = rqMsg.splitlines()
        lines = [x for x in lines if not self.is_line_comment(x)]
        return '\n'.join(map(str,lines))
    

        
    # insert eval into wordlist expressions e.g: {{ string }} to {{ eval(string) }}
    # this is for corpora_context to execute eval function to build up the corpora_context base on wordlist-type
    def inject_eval_func_primitive_wordlist(self, expr: str) -> tuple([bool, str, str]):
        
        try:
        
            tpl = self.jinjaEnvPrimitive.from_string(expr)
            
            output = tpl.render(WordlistTypeHelper.jinja_primitive_wordlist_types_dict())   #tpl.render(self.jinja_primitive_wordlist_types_dict())                
                    
            return True, '', output
        
        except Exception as e:
            return False, e,  expr
   
    
    # *** jinja filters and functions
    
    def jinja_image_func(self, filename=''):
        
        self.currentFuzzCaseSet.file = FuzzCaseSetFile(wordlist_type=WordlistType.image, filename=filename)
        self.currentFuzzCaseSet.fileName = filename
        self.currentFuzzCaseSet.fileDataTemplate = '{{ eval(wordlist_type=\'image\') }}'
        
        return ''
        
    def jinja_pdf_func(self, filename=''):
        
        self.currentFuzzCaseSet.file = FuzzCaseSetFile(wordlist_type=WordlistType.pdf, filename=filename)
        self.currentFuzzCaseSet.fileName = filename
        self.currentFuzzCaseSet.fileDataTemplate = '{{ eval(wordlist_type=\'pdf\') }}'
        
        return ''
        
    def jinja_file_func(self, filename=''):
        
        self.currentFuzzCaseSet.file = FuzzCaseSetFile(wordlist_type=WordlistType.file, filename=filename)
        self.currentFuzzCaseSet.fileName = filename
        self.currentFuzzCaseSet.fileDataTemplate = '{{ eval(wordlist_type=\'file\') }}'
        
        return ''
    
    def jinja_numrange_func(self, start=1, end=100000):
        return  f'{{{{ eval(wordlist_type=\'numrange\', autonumStart={start}, autonumEnd={end}) }}}}'
    
    # insert my wordlist type
    def mutate_jinja_filter(self, value):
        
        # escape single quote if any
        value = value.replace("'", "\\'")
        
        evalOutput = f'{{{{ eval(wordlist_type=\'mutate\', mutate_value=\'{value}\') }}}}' #, my_uniquename=\'{my_uniquename}\') }}}}'
              
        return evalOutput
            
    
    def myfile_jinja_filter(self, content: str, filename: str):
        
        try:
            escapedContent = content.replace('"', '\\"')
        
            ok, err, output = self.inject_eval_func_primitive_wordlist(escapedContent)
            
            if not ok:
                self.eventstore.emitErr(err, data=f'source: requestmessage_fuzzcontext_creator.myfile_jinja_filter')
                self.currentFuzzCaseSet.file = FuzzCaseSetFile(
                    wordlist_type = WordlistType.myfile, #corporaContextKeyName, #
                    filename = filename, #corporaContextKeyName,
                    content = '' )
                self.currentFuzzCaseSet.fileName = filename
                self.currentFuzzCaseSet.fileDataTemplate = ''
                    
                return ''
            
            output = output.strip()
            
            # disable jinja auto-escaping html special characters
            jinjaTpl = f'{{% autoescape false %}}{output}{{% endautoescape %}}'
            
            jinjaTpl = jinjaTpl.strip()
            
            evalOutput =  f'{{{{ eval(wordlist_type="{WordlistType.myfile}", my_file_content_value="{jinjaTpl}", my_file_content_filename="{filename}") }}}}'
            
            # used in corpora_context to find myfile_corpora to supply myfile data
            corporaContextKeyName = f'{WordlistType.myfile}_{filename}'
            
            # *create file object in current fuzzcaseset
            self.currentFuzzCaseSet.file = FuzzCaseSetFile(
                    wordlist_type = WordlistType.myfile, #corporaContextKeyName, #
                    filename = filename, #corporaContextKeyName,
                    content = evalOutput )
            self.currentFuzzCaseSet.fileName = filename
            self.currentFuzzCaseSet.fileDataTemplate = evalOutput
                
            return ''
        except Exception as e:
            pass
        
    
    # check if user has forgotten to put parentheses for file wordlist
    # 
    def is_rendered_body_has_func(self, renderedBody: str):
        if 'RequestMessageFuzzContextCreator' in renderedBody:
            return True
        return False
    
    #refactored, move to "wordlist_type_helper.py"
    # integer type is to support OpenApi3, but is same as digit
    # def jinja_primitive_wordlist_types_dict(self) -> dict:
    #     return {
    #         'string': '{{ eval(wordlist_type=\'string\') }}',
    #         'xss': '{{ eval(wordlist_type=\'xss\') }}',
    #         'sqlinject': '{{ eval(wordlist_type=\'sqlinject\') }}',
    #         'bool':  '{{ eval(wordlist_type=\'bool\') }}',
    #         'digit': '{{ eval(wordlist_type=\'digit\') }}',
    #         'integer': '{{ eval(wordlist_type=\'integer\') }}',
    #         'char': '{{ eval(wordlist_type=\'char\') }}',
    #         'filename': '{{ eval(wordlist_type=\'filename\') }}',
    #         'datetime': '{{ eval(wordlist_type=\'datetime\') }}',
    #         'date': '{{ eval(wordlist_type=\'date\') }}',
    #         'time': '{{ eval(wordlist_type=\'time\') }}',
    #         'username': '{{ eval(wordlist_type=\'username\') }}',
    #         'password': '{{ eval(wordlist_type=\'password\') }}'
    #     }
    
    def is_grapgql(self, headers: dict):
        if Utils.isNoneEmpty(headers) or len(headers) == 0:
            return False
        
        xreqType = 'X-Request-Type'.lower()
        
        for k in headers.keys():
            if xreqType == k.lower():
                return True
       
        return False
            
           
    
    

        
        
            
        
                
        
            
            
        
        
        
        
        
    