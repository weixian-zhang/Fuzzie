# import sys

# print('__main__.py hello')
# print(sys.argv)

# from default_fuzzer import DefaultFuzzer

# fuzzie = DefaultFuzzer(openapiUrl="")
# fuzzie.fuzz()

def fuzz():
    from default_fuzzer import DefaultFuzzer
    import sys
    fuzzie = DefaultFuzzer(openapiUrl="")
    fuzzie.fuzz()
    
    
if __name__ == "__main__":
    fuzz()