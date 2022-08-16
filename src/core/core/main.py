usage = '''

Fuzzie Fuzzer Cli

Usage:
    main.py fuzz [--openapi-url=<url>] [--openapi-path=<filepath>] [--rt=<request-text-string>] [--rt-path=<request-text-path>] 
'''

from docopt import docopt
from default_fuzzer import DefaultFuzzer

def fuzz():
    
    args = docopt(usage)
    
    print(args)
    
    openapiUrl = args['--openapi-url']
    openapiFilePath = args['--openapi-path']
    requestTextSingleString = args['--rt']
    requestTextFilePath = args['--rt-path']
    
    if (not openapiUrl 
        and not openapiFilePath 
        and not requestTextSingleString
        and not requestTextFilePath):
        print('fuzzie fuzzer receive empty arguments')
        return
    
    
    fuzzie = DefaultFuzzer(openapiUrl=openapiUrl, 
                           openapiFilePath=openapiFilePath,
                           requestTextFilePath=requestTextSingleString,
                           requestTextSingleString=requestTextFilePath)
    fuzzie.fuzz()
    
    
if __name__ == "__main__":
    fuzz()