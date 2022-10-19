import unittest

import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
datafactoryPath = os.path.join(currentDir, 'datafactory')
sys.path.insert(0, datafactoryPath)
modelPath = os.path.join(currentDir, 'models')
sys.path.insert(0, modelPath)
apidisPath = os.path.join(currentDir, 'api_discovery')
sys.path.insert(0, apidisPath)

from servicemanager import ServiceManager

class TestServiceManager(unittest.TestCase):
    
    def test_get_fuzzcontexts(self):
        sm = ServiceManager()
        
        fcs = sm.get_fuzzcontexts()
        
        self.assertTrue(fcs is not None)
        
        self.assertTrue(len(fcs) > 0)
    
    def test_get_fuzzcontext_by_Id(self):
        
        Id = 'nnqjyXTtaiT4Wvgx7db7nZ'
        
        sm = ServiceManager()
        
        fc = sm.get_fuzzcontext(Id)
        
        self.assertTrue(fc is not None)
        
    
        
    def test_fuzz(self):
        
        Id = 'nnqjyXTtaiT4Wvgx7db7nZ'
        
        sm = ServiceManager()
        
        sm.fuzz(Id)
        
        
if __name__ == '__main__':
    unittest.main()