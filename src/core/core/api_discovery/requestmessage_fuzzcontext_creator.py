import os,sys
from pathlib import Path
import shortuuid
from datetime import datetime
from urllib.parse import urlparse
import json



parentFolderOfThisFile = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, parentFolderOfThisFile)
sys.path.insert(0, os.path.join(parentFolderOfThisFile, 'models'))

from core.template_helper import TemplateHelper

import re
import validators
from utils import Utils
from models.webapi_fuzzcontext import (ApiFuzzCaseSet, ApiFuzzContext, FuzzCaseSetFile, WordlistType)
from eventstore import EventStore

    
class RequestMessageFuzzContextCreator:

    
    def __init__(self):
        self.apicontext = None
        self.fuzzcontext = ApiFuzzContext()
        self.eventstore = EventStore()
        self.verbs = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
        
        self.detectedJinjaVariables = ''
        
        # currentFuzzCaseSet:
        # use for jinja filters to access current processing fuzzcaseset
        # for now, used by only myfile filter
        self.currentFuzzCaseSet: ApiFuzzCaseSet = None
        
        self.jinjaEnvPrimitive  = TemplateHelper.create_jinja_primitive_env(
            mutate_jinja_filter=self.mutate_jinja_filter,
            jinja_randomize_items_filter=self.jinja_randomize_items_filter,
            jinja_numrange_func=self.jinja_numrange_func,
            jinja_base64e_filter=self.jinja_base64e_filter,
            jinja_base64d_filter=self.jinja_base64d_filter)
        
        self.jinjaEnvBody = TemplateHelper.create_jinja_body_env(mutate_jinja_filter=self.mutate_jinja_filter,
                                                                     myfile_jinja_filter=self.myfile_jinja_filter,
                                                                     jinja_randomize_items_filter=self.jinja_randomize_items_filter,
                                                                     jinja_file_func=self.jinja_file_func,
                                                                     jinja_image_func=self.jinja_image_func,
                                                                     jinja_pdf_func=self.jinja_pdf_func,
                                                                     jinja_numrange_func=self.jinja_numrange_func,
                                                                     jinja_base64e_filter=self.jinja_base64e_filter,
                                                                     jinja_base64d_filter=self.jinja_base64d_filter)
  

    def new_fuzzcontext(self,  
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
            ok, error, fcSets, jinjaVariables = self.parse_request_msg_as_fuzzcasesets(requestTextContent)
        
            if not ok or len(fcSets) == 0:
                return False, error, ApiFuzzContext()
            
            fuzzcontext = ApiFuzzContext()
            fuzzcontext.Id = shortuuid.uuid()
            if name == '':
                fuzzcontext.name = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            else:
                fuzzcontext.name = name
                
            fuzzcontext.datetime = datetime.now()
            fuzzcontext.requestTextContent = requestTextContent
            fuzzcontext.requestMessageFilePath = requestTextFilePath
            fuzzcontext.openapi3FilePath = openapi3FilePath
            fuzzcontext.openapi3Content = openapi3Content
            fuzzcontext.openapi3Url = openapi3Url
            fuzzcontext.authnType = authnType
            fuzzcontext.fuzzcaseToExec = fuzzcaseToExec
            
            fuzzcontext.basicUsername = basicUsername
            fuzzcontext.basicPassword= basicPassword
            fuzzcontext.bearerTokenHeader= bearerTokenHeader
            fuzzcontext.bearerToken= bearerToken 
            fuzzcontext.apikeyHeader=  apikeyHeader 
            fuzzcontext.apikey= apikey
            
            fuzzcontext.fuzzcaseSets = fcSets
            
            fuzzcontext.templateVariables = jinjaVariables
            
            return True, '', fuzzcontext
        
        except Exception as e:
            self.eventstore.emitErr(e)
    
    # request message already contains variables
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
        
        
        ok, error, fcsList, _ = self.parse_request_msg_as_fuzzcasesets(singleRQBlock)
        
        fcsSingleResult = None
        if ok and len(fcsList) > 0:
            fcsResult = fcsList[0]
            
        return True, '', fcsResult
        
    # request message already contains variables
    def parse_request_msg_as_fuzzcasesets(self, rqMsg: str) -> tuple([bool, str, list[ApiFuzzCaseSet], str]):


        if rqMsg == '' or rqMsg.strip() == '':
            return True, '', []
        
        fcSets = []
        
        rqMsgWithoutComments = self.remove_all_comments(rqMsg)
        
        rqMsgWithoutVars, jinjaVariables = self.get_jinja_variables(rqMsgWithoutComments)
        
        #set in global variable so that Jinja filter function can access
        self.detectedJinjaVariables = jinjaVariables
        
        # split request-blocks by delimiter ###
        requestBlocks = rqMsgWithoutVars.strip().split('###')
        
        # each block is a fuzzcaseset
        for eachReqBlock in requestBlocks:
            
            eachReqBlock = eachReqBlock.strip()
            
            if eachReqBlock == '':
                continue
            
            # in 1 req message block, split it multi-line
            multilineBlock: list[str] = eachReqBlock.splitlines()
            
            if len(multilineBlock) == 0:
                return True, '', fcSets, ''

            # remove all breaklines until first char is found
            multilineBlock = self.remove_breaklines_until_char_detected(multilineBlock)
            
            if len(multilineBlock) == 0:
                return False, 'Request Message contains no fuzz case sets', [], ''
            
            # start request-message parsing
            fuzzcaseSet = ApiFuzzCaseSet()
            fuzzcaseSet.Id = shortuuid.uuid()
            self.currentFuzzCaseSet = fuzzcaseSet
            self.currentFuzzCaseSet.requestMessage = eachReqBlock
            
            # get verb
            self.currentFuzzCaseSet.verb = self.get_verb(multilineBlock)
            
            # get url without query
            urlWithoutQS = self.get_url_without_querystring(multilineBlock)
            
            # get query
            lineIndex, qs = self.get_query(multilineBlock)
            
            # full url
            url = f'{urlWithoutQS}{qs}'.strip()
            
            # render url template
            urlOK, urlErr, urlRendered = self.inject_eval_func_primitive_wordlist(url)
            if not urlOK:
                return False, urlErr, [], ''
            
            
            self.currentFuzzCaseSet.urlNonTemplate = url
            self.currentFuzzCaseSet.urlDataTemplate = urlRendered
            
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
                            return hOK, f'Header parsing error: {Utils.errAsText(hErr)}', [], ''
                        
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
                   ok, error, gqlBody, graphqlVariable = self.graphql_get_body_and_variable(multilineBlock)
                   
                   if ok:
                       
                        gqlBody = TemplateHelper.add_global_vars(tpl=gqlBody, vars=self.detectedJinjaVariables)
                        
                        bok, berr, renderedBody = self.inject_eval_func_primitive_wordlist(gqlBody)
                        
                        if not bok:
                            return False, berr, [], ''
                        
                        graphqlVariable = TemplateHelper.add_global_vars(tpl=graphqlVariable, vars=self.detectedJinjaVariables)
                        
                        vok, verr, renderedGQLVar = self.inject_eval_func_primitive_wordlist(graphqlVariable)
                        
                        if not vok:
                            return False, verr, [], ''
                        
                        self.currentFuzzCaseSet.isGraphQL = True
                        self.currentFuzzCaseSet.graphQLVariableNonTemplate = graphqlVariable
                        self.currentFuzzCaseSet.graphQLVariableDataTemplate = renderedGQLVar
                        self.currentFuzzCaseSet.bodyNonTemplate = gqlBody
                        self.currentFuzzCaseSet.bodyDataTemplate = renderedBody
                   else:
                       return False, error, [], ''
                else:
                    
                    body = self.get_body_as_one_str(multilineBlock)
                
                    body = TemplateHelper.add_global_vars(tpl=body, vars=self.detectedJinjaVariables)
                    
                    # jinja wil execute all filters and file-functions bind to image, pdf, file and myfile
                    # if body contains file wordlist, then body will be empty
                    tpl = self.jinjaEnvBody.from_string(body)
                    renderedBody = tpl.render(TemplateHelper.jinja_primitive_wordlist_types_dict()) #tpl.render(self.jinja_primitive_wordlist_types_dict())
                    
                    if self.is_rendered_body_has_func(renderedBody):
                        return False, 'missing parentheses for file wordlist type. e.g: {{ image() }} {{ pdf() }} {{ file() }} {{ '' | myfile() }}', [] , ''

                    # no file found in body
                    if not self.currentFuzzCaseSet.has_file_to_upload(): #Utils.isNoneEmpty(self.currentFuzzCaseSet.file):
                        self.currentFuzzCaseSet.bodyDataTemplate = renderedBody
                        self.currentFuzzCaseSet.bodyNonTemplate = body
                    # *has file in body containing file kind myfile, file, image or pdf
                    else:
                        if self.currentFuzzCaseSet.file == WordlistType.myfile and self.currentFuzzCaseSet.fileDataTemplate == '':
                            return False, 'error when parsing file-content myfile wordlist,', [], ''
                            
                        self.currentFuzzCaseSet.bodyNonTemplate = ''
                        self.currentFuzzCaseSet.bodyDataTemplate = ''           

            fcSets.append(self.currentFuzzCaseSet)
            
        return True, '', fcSets, self.detectedJinjaVariables
    
    def get_url_without_querystring(self, multilineBlock) -> str:
        
        if len(multilineBlock) >= 1:
            
            requestLine: str = multilineBlock[0]
            
            # remove verb
            requestLine = self.remove_verb_if_exist(requestLine)
            
            # remove HTTP/1.1 if any
            requestLine = requestLine.replace('HTTP/1.1', '')
            
            urlonly = requestLine.strip()
            
            if '?' in urlonly:
                urlWithQS = urlonly.split('?')
                urlonly = urlWithQS[0]
            
            return urlonly.strip()
            
        return '', ''
    
    def parse_hostname_port(self, url) -> tuple([bool, str, str, int]):
        
        path = ''
        
        if len(url) >= 1:
                        
            # remove verb
            url = self.remove_verb_if_exist(url)
            
            # remove HTTP/1.1 if any
            url = url.replace('HTTP/1.1', '')
            
            urlonly = url.strip()
            
            parseOutput = urlparse(urlonly)
            url = parseOutput.geturl()
            scheme = parseOutput.scheme if parseOutput.scheme is not None else ''
            hostname = parseOutput.hostname if parseOutput.hostname is not None else ''
            port = parseOutput.port if parseOutput.port is not None else -1
                
            hostname = f'{scheme}://{hostname}'
            
            if not validators.url(hostname):
                return False, f'Invalid url {urlonly}', hostname, port
            
            return True, '', hostname, port
                
        return True, '', '', -1
    
    
     # examples
     # GET https://example.com/comments?page=2
        # &pageSize=10
     #or
     # GET https://example.com/comments
        # ?page=2
        # &pageSize=10
    def get_query(self, multilineBlock) -> tuple([int, str]):
        
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
        
        if '###' in line:
            return False
        
        if line.startswith('//') or line.startswith('#'):
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
    
    def get_jinja_variables(self, rqMsg: str) -> tuple([str,str]): 
        lines = rqMsg.splitlines()
        variables = [x.strip() for x in lines if x.startswith('{%')]
        withoutVar = [x.strip() for x in lines if not x.startswith('{%')]
        
        vars = '\n'.join(map(str,variables))
        rqMsgWithoutVars = '\n'.join(map(str,withoutVar))
        
        return [rqMsgWithoutVars.strip(), vars.strip()]
    
    def remove_all_comments(self, rqMsg: str) -> str: 
        
        lines = rqMsg.splitlines()
        lines = [x for x in lines if not self.is_line_comment(x)]
        return '\n'.join(map(str,lines))

        
    # insert eval into wordlist expressions e.g: {{ string }} to {{ eval(string) }}
    # this is for corpora_context to execute eval function to build up the corpora_context base on wordlist-type
    def inject_eval_func_primitive_wordlist(self, expr: str) -> tuple([bool, str, str]):
        
        try:
                 
            tpl = self.jinjaEnvPrimitive.from_string(expr)
            
            output = tpl.render(TemplateHelper.jinja_primitive_wordlist_types_dict())   #tpl.render(self.jinja_primitive_wordlist_types_dict())                
                    
            return True, '', output.strip()
        
        except Exception as e:
            return False, Utils.errAsText(e),  expr
                
    
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
    
    # value can be a list of strings or single string
    def jinja_base64e_filter(self, value):
        
        cVal = ''
        
        if type(value) is list:
           cVal = '```'.join(value)
        else:
           cVal = str(value)
           
        return  f'{{{{ eval(wordlist_type=\'base64e\', base64eValue=\'{cVal}\') }}}}'
    
    # value can be a list of strings or single string
    # use backtick as delimiter is rare string type and should not conflict with user input
    def jinja_base64d_filter(self, value):
        
        cVal = ''
        
        if type(value) is list:
           cVal = '```'.join(value)
        else:
           cVal = str(value)
           
        return  f'{{{{ eval(wordlist_type=\'base64d\', base64dValue=\'{cVal}\') }}}}'
    
    # insert my wordlist type
    def mutate_jinja_filter(self, value):
        
        # escape single quote if any
        value = value.replace("'", "\\'")
        
        evalOutput = f'{{{{ eval(wordlist_type=\'mutate\', mutate_value=\'{value}\') }}}}' #, my_uniquename=\'{my_uniquename}\') }}}}'
              
        return evalOutput
    
    # take only 100 items
    def jinja_randomize_items_filter(self, items):
        
        itemLimit = 100
        
        itemList = []
        
        if len(items) > itemLimit:
            for idx in range(0,itemLimit -1):
                itemList.append(items[idx])
        else:
            itemList = items
        
        
        mappedItems = map(str, itemList)
        
        itemsStr = ','.join(mappedItems)
        return f'{{{{ eval(wordlist_type=\'random\', randomItemsStr=\'{itemsStr}\') }}}}'
            
    
    def myfile_jinja_filter(self, content: str, filename: str):
        
        try:
            escapedContent = content.replace('"', '\\"')
            
            escapedContent = TemplateHelper.add_global_vars(tpl=escapedContent, vars=self.detectedJinjaVariables)
        
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
            
           
    
    

        
        
            
        
                
        
            
            
        
        
        
        
        
    