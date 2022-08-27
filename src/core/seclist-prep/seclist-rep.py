from naughty_file_generator import NaughtyFilesGenerator
import pandas as pd
import sqlite3
from contextlib import closing
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


prepare_naughty_files(cursor)

#*** naughty files prep complete


# download rest of strings, digits, usernames, passwords
    #insert into db


sqliteconn.close()


