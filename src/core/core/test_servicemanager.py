import unittest

import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
corporafactoryPath = os.path.join(currentDir, 'corporafactory')
sys.path.insert(0, corporafactoryPath)
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
    
    def test_get_fuzzcontext_by_Id(self):
        
        Id = 'BhJZtrRM6HiXtfPtsvdYD2'
        
        sm = ServiceManager()
        
        fc = sm.get_fuzzcontext(Id)
        
        self.assertTrue(fc is not None)
        
    
    def test_fuzz(self):
        
        Id = 'BhJZtrRM6HiXtfPtsvdYD2'
        
        sm = ServiceManager()
        
        sm.fuzz(Id)
        
        
if __name__ == '__main__':
    unittest.main()