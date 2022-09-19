
import sys
from datagen import DataGenerator

class NumericGenerator(DataGenerator):
    
    def __init__(self):
        
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
        
        self.piLargerIntegerFileName = 'data/pi-large.txt'
        
        self.data.append(self.load_from_file(self.piLargerIntegerFileName))
        
        

            
            
    
    # def generate_numeric_values(self, noOfRowsToPad = 1000) -> pd.DataFrame:
        
    #     df = pd.DataFrame()
        
    #     numericDF = self.load_numerics_from_seclist(df)
        
    #     largePIIDF = self.load_superlarge_integer_from_seclist(df)
        
    #     mergedDF = pd.DataFrame()
        
    #     mergedDF = pd.concat([mergedDF, numericDF, largePIIDF])
        
        #return mergedDF
    
    def load_from_file(self, filepath):
        
        with open(filepath) as f:
            lines = f.readlines()
            
            return lines
    
if __name__ == "__main__":
    ng = NumericGenerator()
    
    data = ng.NextData()
        
    # def load_numerics_from_seclist(self, df: pd.DataFrame):
        
    #     #filePath = self.sm.get_file_names_of_directory()
    #     content = self.sm.download_file_as_str(self.numeric_fieldsFileName)
    #     decoded = content.decode('utf-8')
        
    #     splitted = decoded.split('\n')
        
    #     for s in splitted:
    #         df = df.append({"content": s}, ignore_index=True)
            
    #     return df
    
    # def load_superlarge_integer_from_seclist(self, df: pd.DataFram):
        
    #     #filePath = self.sm.get_file_names_of_directory()
    #     content = self.sm.download_file_as_str(self.piLargerIntegerFileName)
    #     decoded = content.decode('utf-8')
    #     splitted = decoded.split('\n')
        
    #     for s in splitted:
    #         df = df.append({"content": s}, ignore_index=True)
            
    #     return df
    
    