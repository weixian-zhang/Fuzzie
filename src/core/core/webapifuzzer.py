
# supported type expression
# openapi3 types
    # {{ string }} (this includes dates and files)
    # {{ number }} (treated as Fuzzie digit)
    # {{ integer }} (treated as Fuzzie digit)
    # {{ boolean }}
# in addition, fuzzie types
    # {{ datetime }}
    # {{ username }}
    # {{ password }}
    # {{ digit }}   (fuzz with integer and float)

import jinja2
from datafactory.hacked_password_generator import HackedPasswordGenerator
from datafactory.hacked_username_generator  import HackedUsernameGenerator
from datafactory.naughty_file_generator import NaughtyFileGenerator
from datafactory.naughty_datetime_generator import NaughtyDateTimeGenerator
from datafactory.naughty_digits_generator import NaughtyDigitGenerator
from datafactory.naughty_string_generator import NaughtyStringGenerator
from datafactory.naughty_bool_generator import NaughtyBoolGenerator
from datafactory.obedient_data_generators import ObedientCharGenerator, ObedientFloatGenerator, ObedientIntegerGenerator, ObedientStringGenerator
from models.webapi_fuzzcontext import ApiFuzzContext, ApiFuzzCaseSet

class WebApiFuzzer:
    
    def __init__(self, apifuzzcontext: ApiFuzzContext) -> None:
        self.apifuzzcontext = apifuzzcontext
    
    
    def test_transform(self):
        
        microTypeTemplates = {
            "string": "{{ getFuzzData('string') }}",
            "number": "{{ getFuzzData('digit') }}",
            "integer": "{{ getFuzzData('digit') }}",
            "digit": "{{ getFuzzData('digit') }}",
            "boolean": "{{ getFuzzData('boolean') }}",
            "datetime": "{{ getFuzzData('datetime') }}",
            "username": "{{ getFuzzData('username') }}",
            "password": "{{ getFuzzData('password') }}",
            "file": "{{ getFuzzData('file') }}",
        }
        
        gqlTemplate = '''
        mutation discoverByUrl {
            discoverByOpenapi3Url(name:{{ string }}, hostname: {{ string }}, port: {{ number }}, openapi3Url: {{string}}){
                ok
                apiFuzzContext {
                    Id
                    hostname
                    port
                    fuzzMode
                    fuzzcaseToExec
                    fuzzcaseSets{
                        Id
                        verb
                        path
                        querystringNonTemplate
                        bodyNonTemplate
                    }
                }
            }
            }
        '''
        
        env = jinja2.Environment()
        
        jinjaTemplate: jinja2.Template = env.from_string(gqlTemplate)
        
        resultWithGetFuzzData =  jinjaTemplate.render(microTypeTemplates)
        
        print(resultWithGetFuzzData)
        
        withActualDataTemplate: jinja2.Template = jinja2.Template(resultWithGetFuzzData)
        
        finalResult =  withActualDataTemplate.render({ 'getFuzzData': self.getFuzzData })
        
        print(finalResult)
    
    def getFuzzData(self, type: str):
        print(type)
    
    
    