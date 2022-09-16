from naughty_file_generator import NaughtyFilesGenerator
from naughty_string_generator import NaughtyStringGenerator
from naughty_username_generator import NaughtyUsernameGenerator
from naughty_password_generator import NaughtyPasswordGenerator
import pandas as pd
import sqlite3
import os


create_db_table_naughtyfile = '''
CREATE TABLE IF NOT EXISTS NaughtyFile (
    id integer PRIMARY KEY AUTOINCREMENT,
	Filename TEXT NOT NULL,
	Content TEXT NOT NULL,
    RowNumber integer NOT NULL
);
'''


# files with metadata isLongFileName has no content but with very long file name to break systems that cannot
# handle very long file names
# exclude zipbombs

create_db_table_naughtystring = '''
CREATE TABLE IF NOT EXISTS NaughtyString (
    id integer PRIMARY KEY AUTOINCREMENT,
    Content TEXT NOT NULL,
    RowNumber integer NOT NULL
);

'''

create_db_table_naughty_usernames = '''
CREATE TABLE IF NOT EXISTS NaughtyUsername (
    id integer PRIMARY KEY AUTOINCREMENT,
    Content TEXT NOT NULL,
    RowNumber integer NOT NULL
);
'''

create_db_table_naughty_password= '''
CREATE TABLE IF NOT EXISTS NaughtyPassword (
    id integer PRIMARY KEY AUTOINCREMENT,
    Content TEXT NOT NULL,
    RowNumber integer NOT NULL
);
'''

dbpath = os.getcwd() + "\src\core\core\datafactory\data\seclist.sqlite"

sqliteconn = sqlite3.connect(dbpath, isolation_level=None)

cursor = sqliteconn.cursor()

# cursor.execute("DROP TABLE IF EXISTS NaughtyFile;")
cursor.execute("DROP TABLE IF EXISTS NaughtyString;")
# cursor.execute("DROP TABLE IF EXISTS NaughtyUsername;")
# cursor.execute("DROP TABLE IF EXISTS NaughtyPassword;")

cursor.execute(create_db_table_naughtyfile)
cursor.execute(create_db_table_naughtystring)
cursor.execute(create_db_table_naughty_usernames)
cursor.execute(create_db_table_naughty_password)

#*** prepare naughty files
def prepare_naughty_files():
    generator = NaughtyFilesGenerator()
    df =  generator.generate_naughty_files()
    
    for index, row in df.iterrows():
        filename = row['Filename']
        content = row['Content']
        rowNum = row['RowNumber']
        
        cursor.execute(f'''
                    insert into NaughtyFile (Filename, Content, RowNumber)
                    values ("{filename}", "{content}", {rowNum})
                    ''')
        
def prepare_naughty_string():
    nsgen = NaughtyStringGenerator()
    df =  nsgen.generate_naughty_strings()
    
    for index, row in df.iterrows():
        content = row['Content']
        content = removeDoubleQuotes(content)
        rowNum = row['RowNumber']
        
        try:
            cursor.execute(f'''
                    insert into NaughtyString (Content, RowNumber)
                    values ("{content}", {rowNum})
                    ''')
        except Exception as e:
            print(e)

def prepare_naughty_username():
    generator = NaughtyUsernameGenerator()
    content = removeDoubleQuotes(content)
    df = generator.generate_naughty_usernames()
    
    for index, row in df.iterrows():
        content = row['Content']
        rowNum = row['RowNumber']
        
        try:
            cursor.execute(f'''
                    insert into NaughtyUsername (Content, RowNumber)
                    values ("{content}", {rowNum})
                    ''')
        except Exception as e:
            print(e)

def prepare_naughty_password():
    generator = NaughtyPasswordGenerator()
    content = removeDoubleQuotes(content)
    df = generator.generate_naughty_password()
    
    for index, row in df.iterrows():
        content = row['Content']
        rowNum = row['RowNumber']
        
        try:
            cursor.execute(f'''
                    insert into NaughtyPassword (Content, RowNumber)
                    values ("{content}", {rowNum})
                    ''')
        except Exception as e:
            print(e)

def removeDoubleQuotes(content: str):
    r = content.replace('"', '')
    return r

if __name__ == '__main__':
    
    prepare_naughty_string()
    # prepare_naughty_files()
    # prepare_naughty_username()
    # prepare_naughty_password()
    sqliteconn.close()
    
    print("data loading completed")


