
import sys, os
from datagen import DataGenerator

class NaughtyDigitGenerator(DataGenerator):
    
    def __init__(self):
        
        super().__init__()
        
        self.data= [
                            0.1000000000000000055511151231257827021181583404541015625,
                            16649142472222295162770764775,
                            2.07564741538e+16,
                            3.38800266804e+16,
                            -139333426276771806651771,
                            -1.97684995314e+16,
                            0x481b49d0f8d5a3e7f821066157c37c,
                            9223372036854775807,
                            9223372036854775808,
                            -9223372036854775809,
                            1.79769313486e+308,
                            1.79769313486e+308,
                            2139095040,
                            2.22507385851e-308,
                            sys.maxsize+1,
                            float('inf'),
                            float('Infinity'),
                            float('-Infinity'),
                            float('NaN'),
                            "79228162514264337593543950336L",
                            "79228162514264337593543950336l",
                            "79228162514264337593543950336B"
                           
        ]
        
        # piLargerIntegerFilePath = os.path.join(os.path.dirname(__file__), "data\\pi-large.txt")
        
        # content = self.load_from_file(piLargerIntegerFilePath)
        
        # self.data.append(content[0])
    
    def load_from_file(self, filepath):
        
        with open(filepath) as f:
            lines = f.readlines()
            
            return lines

    
    