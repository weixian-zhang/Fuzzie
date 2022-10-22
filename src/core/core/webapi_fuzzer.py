
# supported type expression
# openapi3 types
    # {{ string }}                  this includes dates and files
    # {{ number }}                  treated as Fuzzie digit
    # {{ integer }}                 treated as Fuzzie digit
    # {{ boolean }}
# in addition, input expression for Request Message
    # {{ my:[myvalue1,myvalue2,3,4] }}  # supply your own input
    # {{ mutate: a quick brown fox }}   # fuzzie mutates your input by add/alter/remove
    # {{ string }}                  
    # {{ number }}                  
    # {{ file }}
    # {{ boolean }}
    # {{ datetime }}
    # {{ username }}                for login bruteforce entry test
    # {{ password }}                for login bruteforce entry test
    # {{ digit }}                   integer and float
    # {{ char }}
    # {{ base64e:value }}
    # {{ base64e }}                 generate base64 encoded random string value
    # {{ hashsha256:value }}        generates a sha256 hash from supplied value

import asyncio
from http import cookiejar
from types import MappingProxyType
import jinja2
import httplib2
import re
import json
import jsonpickle
import shortuuid
from datetime import datetime
from eventstore import EventStore
from datafactory.hacked_password_generator import HackedPasswordGenerator
from datafactory.hacked_username_generator  import HackedUsernameGenerator
from datafactory.naughty_file_generator import NaughtyFileGenerator
from datafactory.naughty_datetime_generator import NaughtyDateTimeGenerator
from datafactory.naughty_digits_generator import NaughtyDigitGenerator
from datafactory.naughty_string_generator import NaughtyStringGenerator
from datafactory.naughty_bool_generator import NaughtyBoolGenerator
from datafactory.obedient_data_generators import ObedientCharGenerator #, ObedientFloatGenerator, ObedientIntegerGenerator, ObedientStringGenerator
from models.webapi_fuzzcontext import ApiFuzzContext, ApiFuzzCaseSet, ApiFuzzDataCase, ApiFuzzRequest, ApiFuzzResponse, FuzzProgressState, FuzzMode
from db import FuzzDataCaseTable, FuzzRequestTable, FuzzResponseTable, insert_api_fuzzdatacase, insert_api_fuzzrequest, insert_api_fuzzresponse
from sqlalchemy.sql import insert

class WebApiFuzzer:
    
    def __init__(self, apifuzzcontext: ApiFuzzContext) -> None:
        
        # supports remember Set-Cookie from response
        #cookie example
        # contain in single header = cookie1=value1;cookie2=value2
        # Set-Cookie: chocolate=chips; expires=Sun, 15-Nov-2009 18:47:08 GMT; path=/; domain=thaorius.net; secure; httponly
        # Set-Cookie: milk=shape
        self.cookiejar = {}
        
        self.eventstore = EventStore()
        self.apifuzzcontext = apifuzzcontext
        self.passwordGenerator = HackedPasswordGenerator()
        self.usernameGenerator = HackedUsernameGenerator()
        self.fileGenerator = NaughtyFileGenerator() 
        self.datetimeGenerator = NaughtyDateTimeGenerator() 
        self.digitGenerator = NaughtyDigitGenerator() 
        self.stringGenerator = NaughtyStringGenerator() 
        self.boolGenerator = NaughtyBoolGenerator() 
        self.usernameGenerator = HackedUsernameGenerator()
        self.CharGenerator = ObedientCharGenerator()

    async def fuzz(self):
        
        if self.apifuzzcontext == None or len(self.apifuzzcontext.fuzzcaseSets) == 0:
            self.eventstore.emitErr(f'WebApiFuzzer detected empty ApiFuzzContext: {self.apifuzzcontext}')
            return
        
        self.eventstore.emitInfo(f'start fuzzing {self.apifuzzcontext.name}')
        
        await self.begin_fuzzing()
        
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete()
        
    async def begin_fuzzing(self):
        
        fuzzCasesToTest = self.determine_no_of_fuzzcases_to_run(self.apifuzzcontext.fuzzMode, self.apifuzzcontext.fuzzcaseToExec)
        
        for fcs in self.apifuzzcontext.fuzzcaseSets:
            
            for fuzzcount in range(0, fuzzCasesToTest):
            
                fuzzCaseData = self.http_fuzz_api(fcs)
                    
                # await self.save_fuzzDataCase(fuzzCaseData)
                
                await self.eventstore.send_to_wsclient(jsonpickle.encode(fuzzCaseData))
                #await self.emit_client_fuzz_status(fuzzCaseData)  
                
    def http_fuzz_api(self, fcs: ApiFuzzCaseSet) -> ApiFuzzDataCase:
        http = httplib2.Http()
                
        fuzzDataCase = self.create_fuzzdatacase(fuzzcaseSetId=fcs.Id,
                                                fuzzcontextId=self.apifuzzcontext.Id)
        
        hostnamePort, url, path, querystring, body, headers = self.dataprep_fuzzcaseset(http, self.apifuzzcontext, fcs)
        
        fuzzrequest = self.create_fuzzrequest(
                                fuzzDataCaseId=fuzzDataCase.Id,
                                fuzzcontextId=self.apifuzzcontext.Id,
                                hostnamePort=hostnamePort,
                                url=url,
                                path=path,
                                qs=querystring,
                                verb=fcs.verb,
                                headers=headers,
                                body=body)
        
        fuzzResp = self.create_fuzzresponse(fuzzDataCase.Id, self.apifuzzcontext.Id)
        
        fuzzDataCase.request = fuzzrequest
        fuzzDataCase.response = fuzzResp
        
        try:
            
            resp, content = http.request(url,
                        fcs.verb, body=body,
                        headers=headers )

            fuzzResp.statusCode = resp.status
            fuzzResp.reasonPharse = resp.reason
            
            respJson, respDict = self.response_as_json(resp.items().mapping)
            
            fuzzResp.responseJson = respJson
            
            fuzzResp.setcookieHeader = self.try_get_setcookie_value(respDict)
            
            #stripped = re.sub('<[^<]+?>', '', )
            fuzzResp.content = content.decode()
            
            self.save_responsecookie_in_cookiejar(hostnamePort, fuzzResp.setcookieHeader)
            
        except Exception as e:
            fuzzResp.content = f'Error when fuzzing {url}, {e.strerror}'
            
        return fuzzDataCase
            
    def response_as_json(self, respMapping: MappingProxyType):
        dict = {}
        for k in respMapping.keys():
            dict[k] = respMapping[k]
        j = json.dumps(dict)
        return [j, dict]
    
    def try_get_setcookie_value(self, respHeadersDict: dict):
        result = ''
        setCookieHeader = 'Set-Cookie'
        if setCookieHeader in respHeadersDict.keys():
            result = respHeadersDict[setCookieHeader]
        return result
                     
    def save_responsecookie_in_cookiejar(self, hostname, cookie):
        if cookie == '':
            return
        
        if not hostname in self.cookiejar.keys():
            self.cookiejar[hostname] = cookie
        
    def dataprep_fuzzcaseset(self, http, fc: ApiFuzzContext, fcs: ApiFuzzCaseSet):
        
        hostnamePort = fc.get_hostname_port()
        pathDT = fcs.get_path_datatemplate()
        querystringDT = fcs.get_querystring_datatemplate()
        bodyDT= fcs.bodyDataTemplate
        headerDT = fcs.headerDataTemplate
        
        path = self.inject_fuzzdata_in_datatemplate(pathDT)
        querystring = self.inject_fuzzdata_in_datatemplate(querystringDT)
        body = self.inject_fuzzdata_in_datatemplate(bodyDT)
        headerStr = self.inject_fuzzdata_in_datatemplate(headerDT)
        headerDict = json.loads(headerStr)
        
        url = f'{hostnamePort}{path}{querystring}'
        
        securityHeaders = {}
        if fc.isAnonymous == False:
            if fc.is_basic_authn():
                http.add_credentials(fc.basicUsername, fc.basicPassword)
            elif fc.is_bearertoken_authn():
                securityHeaders[fc.bearerTokenHeader] = fc.bearerToken
            elif fc.is_apikey_authn():
                securityHeaders[fc.apikeyHeader] = fc.apikey
                
        headers = {**securityHeaders, **headerDict}     #merge 2 dicts
        
        return [hostnamePort, url, path, querystring, body, headers]
        
    
            
    def inject_fuzzdata_in_datatemplate(self, tpl: str) -> str:
        
        if tpl == '':
            return ''
        
        template = jinja2.Template(tpl)
        result =  template.render({ 'getFuzzData': self.getFuzzData })
        return result
            
    def getFuzzData(self, type: str):
        match type:
            case 'string':
                return self.stringGenerator.NextData()
            case 'number':
                return self.digitGenerator.NextData()
            case 'integer':
                return self.digitGenerator.NextData()
            case 'int':
                return self.digitGenerator.NextData()
            case 'digit':
                return self.digitGenerator.NextData()
            case 'bool':
                return self.boolGenerator.NextData()
            case 'username':
                return self.usernameGenerator.NextData()
            case 'password':
                return self.passwordGenerator.NextData()
            case 'char':
                return self.CharGenerator.NextData()
            case 'datetime':
                return self.datetimeGenerator.NextData()
            case 'file':
                return self.fileGenerator.NextData()
            case _:
                return self.stringGenerator.NextData()
    
    async def save_fuzzDataCase(self, fdc: ApiFuzzDataCase):

        try:
            insert_api_fuzzdatacase(fdc)
            insert_api_fuzzrequest(fdc.request)
            insert_api_fuzzresponse(fdc.response)
        except Exception as e:
            self.eventstore.emitErr(f'Error when saving fuzzdatacase, fuzzrequest and fuzzresponse: {e}')
        
    
    async def emit_client_fuzz_status(self, fuzzDataCase):
        self.ee
    
    def create_fuzzdatacase(self, fuzzcaseSetId, fuzzcontextId):
        
        fdc = ApiFuzzDataCase()
        fdc.Id = shortuuid.uuid()
        fdc.fuzzCaseSetId = fuzzcaseSetId
        fdc.fuzzcontextId = fuzzcontextId
        fdc.progressState = FuzzProgressState.FUZZING.name
        return fdc

    def create_fuzzrequest(self, fuzzDataCaseId, fuzzcontextId, hostnamePort, verb, path, qs, url, headers, body):
        
        fr = ApiFuzzRequest()
        
        fr.Id = shortuuid.uuid()
        fr.datetime = datetime.now()
        fr.fuzzDataCaseId = fuzzDataCaseId
        fr.fuzzcontextId =fuzzcontextId
        fr.hostnamePort = hostnamePort
        fr.verb = verb
        fr.path = path
        fr.querystring = qs
        fr.url = url
        fr.headers = json.dumps(headers)
        fr.body = body
        
        return fr
    
    def create_fuzzresponse(self, fuzzDataCaseId, fuzzcontextId):
        fresp = ApiFuzzResponse()
        fresp.Id = shortuuid.uuid()
        fresp.datetime = datetime.now()
        fresp.fuzzDataCaseId = fuzzDataCaseId
        fresp.fuzzcontextId = fuzzcontextId 
        return fresp     
        
        
    # minimum 100 fuzz cases to run
    def determine_no_of_fuzzcases_to_run(self, fuzzmode: str, fuzzcaseToExec):
        
        default = 100
        
        if fuzzmode == FuzzMode.Quick.name:
            return default
        elif fuzzmode == FuzzMode.Full.name:
            return self.stringGenerator.get_dbsize()
        elif fuzzmode == FuzzMode.Custom.name:
            if fuzzcaseToExec <= default:
                return default
            else:
                return fuzzcaseToExec
        
        
        
        
    # def test_transform(self):
        
    #     microTypeTemplates = {
    #         "string": "{{ getFuzzData('string') }}",
    #         "number": "{{ getFuzzData('digit') }}",
    #         "integer": "{{ getFuzzData('digit') }}",
    #         "digit": "{{ getFuzzData('digit') }}",
    #         "boolean": "{{ getFuzzData('boolean') }}",
    #         "datetime": "{{ getFuzzData('datetime') }}",
    #         "username": "{{ getFuzzData('username') }}",
    #         "password": "{{ getFuzzData('password') }}",
    #         "file": "{{ getFuzzData('file') }}",
    #     }
        
    #     gqlTemplate = '''
    #     mutation discoverByUrl {
    #         discoverByOpenapi3Url(name:{{ string }}, hostname: {{ string }}, port: {{ number }}, openapi3Url: {{string}}){
    #             ok
    #             apiFuzzContext {
    #                 Id
    #                 hostname
    #                 port
    #                 fuzzMode
    #                 fuzzcaseToExec
    #                 fuzzcaseSets{
    #                     Id
    #                     verb
    #                     path
    #                     querystringNonTemplate
    #                     bodyNonTemplate
    #                 }
    #             }
    #         }
    #         }
    #     '''
        
    #     env = jinja2.Environment()
        
    #     jinjaTemplate: jinja2.Template = env.from_string(gqlTemplate)
        
    #     resultWithGetFuzzData =  jinjaTemplate.render(microTypeTemplates)
        
    #     print(resultWithGetFuzzData)
        
    #     withActualDataTemplate: jinja2.Template = jinja2.Template(resultWithGetFuzzData)
        
    #     finalResult =  withActualDataTemplate.render({ 'getFuzzData': self.getFuzzData })
        
    #     print(finalResult)
    
    
    
    
    