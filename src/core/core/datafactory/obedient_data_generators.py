
import random
from datagen import DataGenerator

    
class ObedientFloatGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()
        self.lowerLimit = -100000
        self.upperLimit = 100000
        
    def NextData(self):
        min = str(self.lowerLimit) + ".1"
        max = str(self.upperLimit) + ".9"
        return random.uniform(float(min), float(max))
    
class ObedientIntegerGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()
        self.lowerLimit = -100000
        self.upperLimit = 100000
        
    def NextData(self):
        return random.randint(self.lowerLimit, self.upperLimit)

class ObedientCharGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()
        self.lowLowercaseLetterAscii = 65
        self.highExtendedAscii = 255
    
    def NextData(self):
        return chr(random.randrange(self.lowLowercaseLetterAscii, self.highExtendedAscii))
        
    
class ObedientStringGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()
        self.strLength = 100
        self.lowLowercaseLetterAscii = 65
        self.highLowercaseLetterAscii = 90
        self.lowLetterAscii= 97
        self.highLetterAscii = 122
        self.lowExtendedAscii = 128
        self.highExtendedAscii = 255
        
        self.randomer = {
            0: self.generate_random_uppercase_letter_from_ascii,
            1: self.generate_random_lowercase_letter_from_ascii,
            2: self.generate_random_integer,
            3: self.generate_random_special_char_from_ascii
        }
        
    def generate_random_special_char_from_ascii(self):
            return chr(random.randrange(self.lowExtendedAscii, self.highExtendedAscii))

    def generate_random_uppercase_letter_from_ascii(self):
        return chr(random.randrange(self.lowLetterAscii, self.highLetterAscii))

    def generate_random_lowercase_letter_from_ascii(self):
        return chr(random.randrange(self.lowLowercaseLetterAscii, self.highLowercaseLetterAscii))

    def generate_random_integer(self):
        return random.randint(0, 9)

    def NextData(self):
    
        '''
            A string contains first-half numbers and letters, second-half contains special symbols and chars,
            hence, diving string into 2 parts
            ref: https://www.asciitable.com/
        '''
        
        randomer = {
            0: self.generate_random_uppercase_letter_from_ascii,
            1: self.generate_random_lowercase_letter_from_ascii,
            2: self.generate_random_integer,
            3: self.generate_random_special_char_from_ascii
        }
        
        randomHighLimit = 3
            
        rs = ""
        for c in range(0, self.strLength ):
            rs = rs + str(randomer[random.randint(0, randomHighLimit)]())
            
        return rs
        
# if __name__ == '__main__':
#     pass
#     a = ObedientBoolGenerator()
#     r1 = a.NextData()
#     r1 = a.NextData()
#     r1 = a.NextData()
#     r1 = a.NextData()
#     r1 = a.NextData()
#     r1 = a.NextData()
#     r1 = a.NextData()
#     r1 = a.NextData()
#     r1 = a.NextData()
    
    
#     b = ObedientCharGenerator()
#     r2 = b.NextData()
#     r2 = b.NextData()
#     r2 = b.NextData()
#     r2 = b.NextData()
#     r2 = b.NextData()
    
#     c = ObedientFloatGenerator()
#     r3 = c.NextData()
#     r3 = c.NextData()
#     r3 = c.NextData()
#     r3 = c.NextData()
#     r3 = c.NextData()
#     r3 = c.NextData()
    
    
#     d = ObedientIntegerGenerator()
#     r4 = d.NextData()
#     r4 = d.NextData()
#     r4 = d.NextData()
#     r4 = d.NextData()
#     r4 = d.NextData()
    
    
#     f = ObedientStringGenerator()
#     r5 = f.NextData()
#     r5 = f.NextData()
#     r5 = f.NextData()
#     r5 = f.NextData()
#     r5 = f.NextData()
#     r5 = f.NextData()
        

