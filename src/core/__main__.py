
# fuzzie-core is package as zip file and client executes fuzzie.zip and by default executes __main__.py

from fuzzie_core import Fuzzie
import sys

def fuzz(openapiUrl: str):
    fuzzie = Fuzzie(openapiUrl=openapiUrl)
    fuzzie.fuzz()
    
if __name__ == "__main__":
    #fuzz(sys.argv)
    print(sys.argv)