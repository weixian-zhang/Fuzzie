#import all sub directories
import sys, os
# print([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])
# sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

#from default_fuzzer import DefaultFuzzer

def fuzz():
    
    from default_fuzzer import DefaultFuzzer
    fuzzie = DefaultFuzzer(openapiUrl="")
    fuzzie.fuzz()
    
    
if __name__ == "__main__":
    fuzz()