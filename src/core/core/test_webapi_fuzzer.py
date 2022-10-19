
import unittest

import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
datafactoryPath = os.path.join(currentDir, 'datafactory')
sys.path.insert(0, datafactoryPath)
modelPath = os.path.join(currentDir, 'models')
sys.path.insert(0, modelPath)

from webapifuzzer import WebApiFuzzer

class TestWebApiFuzzer(unittest.TestCase):
               
            
    def test_transform(self):
        
        fuzzer = WebApiFuzzer(None)
        
        fuzzer.test_transform()
        
        
if __name__ == "__main__":
    unittest.main()