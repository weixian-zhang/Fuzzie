import random

class ListUtils:
    
    def pad_rows(dataList, noOfRowsToPad = 1000) -> list:
        
        listlength = len(dataList)
        
        if noOfRowsToPad <= listlength:
            return dataList
        
        paddedList = dataList[:]
        
        
        rowsToPad = noOfRowsToPad - listlength
        
        for i in range(rowsToPad):
            
            randIndex = random.randint(0, listlength -1)
            val = dataList[randIndex]
            
            paddedList.append(val)
                   
        return paddedList