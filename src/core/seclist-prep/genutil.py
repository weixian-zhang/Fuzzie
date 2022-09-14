
import random


def generate_random_float(rowsToGen = 10) -> list[int]:
    
    result = []
    for x in range(0, rowsToGen):
        minInt = random.randint(-10000, 10000)
        maxInt = random.randint(10001, 100000)
        min = str(minInt) + ".1"
        max = str(maxInt) + ".9"
        result.append(random.uniform(float(min), float(max)))
        
    return result

def generate_random_int(rowsToGen = 10) -> list[int]:
    
    result = []
    for x in range(0, rowsToGen):
        randint = random.randint(-100000, 100000)
        result.append(randint)
        
    return result



lowDigitAscii = 48
highDigitAscii = 57
lowLowercaseLetterAscii = 65
highLowercaseLetterAscii = 90
lowLetterAscii= 97
highLetterAscii = 122
lowExtendedAscii = 128
highExtendedAscii = 255

def generate_random_special_char_from_ascii():
    return chr(random.randrange(lowExtendedAscii, highExtendedAscii))

def generate_random_uppercase_letter_from_ascii():
    return chr(random.randrange(lowLetterAscii, highLetterAscii))

def generate_random_lowercase_letter_from_ascii():
    return chr(random.randrange(lowLowercaseLetterAscii, highLowercaseLetterAscii))

def generate_random_integer():
    return random.randint(0, 9)

def generate_random_meaningless_string(length=100, rows=50, includeSpecialChar=False):
    
    '''
        A string contains first-half numbers and letters, second-half contains special symbols and chars,
        hence, diving string into 2 parts
        ref: https://www.asciitable.com/
    '''
    
    randomer = {
        0: generate_random_uppercase_letter_from_ascii,
        1: generate_random_lowercase_letter_from_ascii,
        2: generate_random_integer,
        3: generate_random_special_char_from_ascii
    }
    
    randomHighLimit = 2
    
    if includeSpecialChar:
        randomHighLimit = 3
        
    result = [];
    for x in range(0,rows):
        
        rs = ""
        
        #str part 1
        for c in range(0, length):
            rs = rs + str(randomer[random.randint(0, randomHighLimit)]())
            
            
        result.append(rs);
        
    return result
        
        
        
    

if __name__ == '__main__':
    a = generate_random_meaningless_string(includeSpecialChar=False)
    print(a)
