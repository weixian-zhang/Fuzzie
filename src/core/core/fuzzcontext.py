from enum import Enum
from typing import List

class TestCase:
    data = {}
    request = {}
    response = {}

# Also the data to be rendered on Fuzzie GUI client - VSCode extension and future Desktop client. 
class FuzzContext:
    
    def __init__(self) -> None:
        
        self.openapiUrl : str = ""
        self.openapiFilePath : str = ""
        self.requestTextFilePath : str = ""
        self.requestTextSingle : str = ""
        
        self.workingDirectory : str = ""
        
        self.testcases : list[TestCase] = []
        
class FuzzProgressState(Enum):
    NOTSTARTED = "not started"
    FUZZING = "still fuzzing"
    SUCCESS = "complete"
    FAILED = "failed"
    
# Used by GUI clients to update fuzzing progress on each API
class FuzzProgress:
    testcaseId = ""
    state : FuzzProgressState = FuzzProgressState.NOTSTARTED
    pass 