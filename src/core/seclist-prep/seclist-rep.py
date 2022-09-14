from naughty_file_generator import NaughtyFilesGenerator
from naughty_string_generator import NaughtyStringGenerator
from numeric_generator import NumericGenerator

import pandas as pd
import sqlite3
import os
#create all tables

create_db_table_naughtyfile = '''
CREATE TABLE IF NOT EXISTS NaughtyFile (
    id integer PRIMARY KEY AUTOINCREMENT,
	Name TEXT NOT NULL,
	Content TEXT NOT NULL
);
'''


# files with metadata isLongFileName has no content but with very long file name to break systems that cannot
# handle very long file names
# exclude zipbombs

create_db_table_seclist = '''
CREATE TABLE IF NOT EXISTS SecList (
    id integer PRIMARY KEY AUTOINCREMENT,
	NaughtyString TEXT NOT NULL,
	Digit TEXT NOT NULL,
    UserName TEXT NOT NULL,
    Password TEXT NOT NULL
);
'''

dbpath = os.getcwd() + "\src\core\seclist-prep\seclist.sqlite"

sqliteconn = sqlite3.connect(dbpath, isolation_level=None)

cursor = sqliteconn.cursor()

cursor.execute("DROP TABLE IF EXISTS NaughtyFile;")
cursor.execute("DROP TABLE IF EXISTS SecList;")

cursor.execute(create_db_table_naughtyfile)

cursor.execute(create_db_table_seclist)

#*** prepare naughty files
def prepare_naughty_files(conn: sqlite3.Cursor):
    naughtyFilesGen = NaughtyFilesGenerator()

    nFilesDF =  naughtyFilesGen.generate_naughty_files()

    for index, row in nFilesDF.iterrows():
        filename = row['filename']
        content = row['content']
        
        cursor.execute(f'''
                    insert into NaughtyFile (Name, Content)
                    values ("{filename}", "{content}")
                    ''')
        
def prepare_naughty_string() -> pd.DataFrame:
    nsgen = NaughtyStringGenerator()
    df =  nsgen.generate_naughty_strings()
    return df

def prepare_naughty_integers() -> pd.DataFrame:
    ngen = NumericGenerator()
    df =  ngen.generate_numeric_values()
    return df
    

def mergeData():
    #nsDF = prepare_naughty_string()
    
    numericDF = prepare_naughty_integers()
    
    mergedDF = pd.DataFrame()
    
    #mergedDF = pd.concat([mergedDF, nsDF])
    
    print(mergedDF)


#prepare_naughty_files(cursor)

mergeData()

#*** naughty files prep complete


# download rest of strings, digits, usernames, passwords
    #insert into db


sqliteconn.close()


