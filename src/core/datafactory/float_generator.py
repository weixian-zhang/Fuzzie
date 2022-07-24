import numpy
from data_factory_utils import DataFactoryUtils

class FloatGenerator:
    
    def __init__(self):
        self.specialData = [-1.7976931348623157e+308, 
                            1.7976931348623157e+308, # min, max floats
                            0.1000000000000000055511151231257827021181583404541015625]
        
    def generate_floats(self, noOfRowsToPad = 1000) -> list:
           
        intSeclist = DataFactoryUtils.load_bad_integers_from_seclist()
        intSeclistLength = len(intSeclist)
        
        if noOfRowsToPad <= intSeclistLength:
            return intSeclist
        
        rowsToPadExcludeSeclistAndSpecialData = (noOfRowsToPad - intSeclistLength) - len(self.specialData)
        
        randFloats = numpy.random.uniform(low=-5000.1, high=10000.5, size=rowsToPadExcludeSeclistAndSpecialData)
        
        merged = self.specialData + intSeclist + [x for x in randFloats]
        
        return merged
        
        
    
    