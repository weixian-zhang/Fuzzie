from datetime import date, time, datetime
from random import random
from dateutil import parser
import time as tTime
import random

#datetime formats
#https://medium.com/analytics-vidhya/dealing-with-date-time-of-different-formats-in-python-f1f973d8cdb
#https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime

#unix time stamp & date manipulation
#https://www.dataquest.io/blog/python-datetime-tutorial/

#time zone
#https://pynative.com/python-timezone/#:~:text=Format%20UTC%20DateTime%20to%20Get,to%20get%20the%20timezone%20name.

#max date, min date

from datagen import DataGenerator

class NaughtyDateTimeGenerator(DataGenerator):
    
    def __init__(self):
        
        super().__init__()
        
        self.naughtyDateTimeSize = 50
        self.data = [
            date.min,
            date(1, 1, 1),
            date(9999, 12, 31),
            date(1904, 1, 1)  ,  #mac system
            date(1601, 1, 1) ,   #Windows system
            tTime.mktime(datetime.now().timetuple()), #unix timestamp
            time(0, 0),
            time(23, 59, 59, 999999),
            datetime(1, 1, 1, 0, 0),
            datetime(9999, 12, 31, 23, 59, 59, 999999),
            datetime.now().date(),
            datetime.now().time(),
        ]
        
        self.generate_datetime_formats()
        
        self.generate_naughty_datetime()
        
    
    def generate_datetime_formats(self):
        
        dateFormats = [
            "%B %d, %Y %A, %H:%M:%S",
            "%B %A %d %Y, %H:%M:%S",
            "%A %B, %H:%M:%S",
            "%d, %H:%M:%S",
            "%d %B %A, %H:%M:%S",
            "%d %A %B, %H:%M:%S",
            "%d-%m-%y %H:%M:%S",
            "%m-%d-%y %H:%M:%S",
            "%y-%m-%d %H:%M:%S",
            "%d/%m/%y %H:%M:%S",
            "%m/%d/%y %H:%M:%S",
            "%y/%m/%d %H:%M:%S",
            "%y %m %d %H:%M:%S",
            "%d %m %y %H:%M:%S",
            "%m %d %y %H:%M:%S",
            
            #time only
            "%H:%M:%S",
            "%I:%M:%S",
            "%H:%M:%S %f",
            "%I:%M:%S %f",
            ]
        
        for df in dateFormats:
            newDF = datetime.now().strftime(df)
            self.data.append(newDF)
    
    def generate_naughty_datetime(self):
        # %a: Weekday as locale’s abbreviated name. sun , mon
        # %A : Weekday as locale’s full name.Sunday, Monday, …
        # %w: Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.
        # %d: Day of the month as a zero-padded decimal number.
        # %b: Month as locale’s abbreviated name. Jan, Feb
        # %B: Month as locale’s full name. January
        # %m: Month as a zero-padded decimal number.
        # %y: Year without century as a zero-padded decimal number.
        # %Y: Year with century as a decimal number.
        # %H: Hour (24-hour clock) as a zero-padded decimal number.
        # %I: Hour (12-hour clock) as a zero-padded decimal number.
        # %p: Locale’s equivalent of either AM or PM.
        # %M: Minute as a zero-padded decimal number.
        # %S: Second as a zero-padded decimal number.
        # %f: Microsecond as a decimal number, zero-padded on the left.
        # %z: UTC offset in the form ±HHMM[SS] (empty string if the object is naive).
        # %Z: Time zone name (empty string if the object is naive).
        # %j: Day of the year as a zero-padded decimal number.
        # %U: Week number of the year (Sunday as the first day of the week) as a zero
        
        dtFormatTokens = ['%a','%A','%w','%d','%b','%B','%m','%y','%Y','%H','%I','%p','%M','%S','%f','%z','%Z','%j','%U']
        
        currentSize = 0
        
        while currentSize <= self.naughtyDateTimeSize:
        
            for i, element in enumerate(dtFormatTokens):
                nformat = f'''{dtFormatTokens[self.random_num(len(dtFormatTokens))]}, {dtFormatTokens[self.random_num(len(dtFormatTokens))]}, {dtFormatTokens[self.random_num(len(dtFormatTokens))]} {dtFormatTokens[self.random_num(len(dtFormatTokens))]} {dtFormatTokens[self.random_num(len(dtFormatTokens))]} {dtFormatTokens[self.random_num(len(dtFormatTokens))]}'''
                nDateTime = newDF = datetime.now().strftime(nformat)

                self.data.append(nDateTime)
            
            currentSize += 1
                
    def random_num(self, dataLength):
        return random.randint(0, dataLength - 1) #-1 for list 0 index
                
                
    
        
            
        
