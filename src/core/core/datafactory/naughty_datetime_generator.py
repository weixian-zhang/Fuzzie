from datetime import date, time, datetime
from dateutil import parser

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
        
        
        self.data = [
            date.min,
            date(1, 1, 1),
            date(9999, 12, 31),
            time(0, 0),
            time(23, 59, 59, 999999),
            datetime(1, 1, 1, 0, 0),
            datetime(9999, 12, 31, 23, 59, 59, 999999),
            datetime.now().date(),
            datetime.now().time()
        ]
        
        self.generate_datetime_formats()
        
    
    def generate_datetime_formats(self):
        
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
        
        dateFormats = [
            # "%B %d, %Y %A, %H:%M:%S",
            #"%B %A %d %Y, %H:%M:%S",
            #"%A %B, %H:%M:%S",
            "%d, %H:%M:%S",
            "%d %B %A, %H:%M:%S",
            "%d %A %B, %H:%M:%S",
            
            "%d-%m-%y %H:%M:%S",
            "%m-%d-%y %H:%M:%S",
            "%y-%m-%d %H:%M:%S",
            "%d/%m/%y %H:%M:%S",
            "%m/%d/%y %H:%M:%S",
            "%y/%m/%d %H:%M:%S",
            
            # "%d-%m-%Y %H:%M:%S",
            # "%m-%d-%Y %H:%M:%S",
            # "%Y-%m-%d %H:%M:%S",
            # "%d/%m/%Y %H:%M:%S",
            # "%m/%d/%Y %H:%M:%S",
            # "%Y/%m/%d %H:%M:%S",
            
            #time only
            "%H:%M:%S",
            "%I:%M:%S",
            "%H:%M:%S %f",
            "%I:%M:%S %f",
            ]
        
        for df in dateFormats:
            newDF = datetime.now().strftime(df)
            print(newDF)
            
            newDFDateTime = parser.parse(newDF)
            self.data.append(newDFDateTime)