# import random
# from storagemanager import StorageManager

# class DataFactoryUtils:
    
#     def pad_rows(dataList, noOfRowsToPad = 1000) -> list:
        
#         listlength = len(dataList)
        
#         if noOfRowsToPad <= listlength:
#             return dataList
        
#         paddedList = dataList[:]
        
        
#         rowsToPad = noOfRowsToPad - listlength
        
#         for i in range(rowsToPad):
            
#             randIndex = random.randint(0, listlength -1)
#             val = dataList[randIndex]
            
#             paddedList.append(val)
                   
#         return paddedList
    
#     # data contains some floats
#     def load_bad_integers_from_seclist() -> list:
        
#         sm = StorageManager()
#         content = sm.download_file_as_str('digit/numeric-fields-only.txt')
#         decoded = content.decode('utf-8')
#         splitted = decoded.split("\n")
        
#         result = []
#         for x in splitted:
            
#             if DataFactoryUtils.is_float(x):
#                 result.append(float(x))
#                 continue
            
#             if DataFactoryUtils.is_int(x):
#                 result.append(int(x))
                
#         result += [x for x in splitted if not DataFactoryUtils.is_float(x) and not DataFactoryUtils.is_int(x)]  
        
#         return result
    
    
#     def is_float(value) -> bool:
#       try:
#         float(value)
#         return True
#       except:
#         return False
    
#     def is_int(value) -> bool:
#       try:
#         int(value)
#         return True
#       except:
#         return False