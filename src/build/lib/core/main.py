#import all sub directories
import sys, os
# print([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])
# sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

#from default_fuzzer import DefaultFuzzer

def fuzz():
    
    # fuzzie = DefaultFuzzer(openapiUrl="")
    # fuzzie.fuzz()
    
    executionPath = os.path.dirname(os.path.realpath(__file__))
    print('hello, project path = ' + executionPath + './api-initmanager')
    
    
if __name__ == "__main__":
    fuzz()