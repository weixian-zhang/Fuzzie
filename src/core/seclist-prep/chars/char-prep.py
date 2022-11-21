import io

f = io.open("chars.txt", mode="r", encoding="utf-8")

lines = f.readlines()
result = []

for line in lines:
    line = line.replace('\n', '')
    
    if len(line) > 1:
        if line.startswith('U+'):
            result.append(line)
            continue
        
        for c in line:
            if c != ' ':
                result.append(c)
    else:
        result.append(line)
        
        
import codecs

file = codecs.open("chars-final.txt", "w", "utf-8")
for line in result:
        file.write(f"{line}\n")
file.close()
                
                
            
        
            