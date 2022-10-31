from naughty_file_generator import NaughtyFilesGenerator
from naughty_string_generator import NaughtyStringGenerator
from naughty_username_generator import NaughtyUsernameGenerator
from naughty_password_generator import NaughtyPasswordGenerator
from naughty_useragent_generator import NaughtyUserAgentGenerator
from naughty_httpheaders_generators import NaughtyHttpHeadersGenerator
import pandas as pd
import sqlite3
import os


# files with metadata isLongFileName has no content but with very long file name to break systems that cannot
# handle very long file names
# exclude zipbombs
create_db_table_naughtyfile = '''
CREATE TABLE IF NOT EXISTS NaughtyFile (
    id integer PRIMARY KEY AUTOINCREMENT,
	Filename TEXT NOT NULL,
	Content TEXT NOT NULL,
    RowNumber integer NOT NULL
);
'''

create_db_table_naughty_httpheaders= '''
CREATE TABLE IF NOT EXISTS NaughtyHttpHeader (
    id integer PRIMARY KEY AUTOINCREMENT,
    Content TEXT NOT NULL,
    RowNumber integer NOT NULL
);

'''


create_db_table_naughtyuseragent= '''
CREATE TABLE IF NOT EXISTS NaughtyUserAgent (
    id integer PRIMARY KEY AUTOINCREMENT,
    Content TEXT NOT NULL,
    RowNumber integer NOT NULL
);

'''

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

dbpath = os.getcwd() + "\src\core\core\datafactory\data\\fuzzie.sqlite"

sqliteconn = sqlite3.connect(dbpath, isolation_level=None)

cursor = sqliteconn.cursor()

# cursor.execute("DROP TABLE IF EXISTS NaughtyHttpHeader;")
# cursor.execute("DROP TABLE IF EXISTS NaughtyUserAgent;")
# cursor.execute("DROP TABLE IF EXISTS NaughtyFile;")
# cursor.execute("DROP TABLE IF EXISTS NaughtyString;")
# cursor.execute("DROP TABLE IF EXISTS NaughtyUsername;")
# cursor.execute("DROP TABLE IF EXISTS NaughtyPassword;")

cursor.execute(create_db_table_naughty_httpheaders)
cursor.execute(create_db_table_naughtyuseragent)
cursor.execute(create_db_table_naughtyfile)
cursor.execute(create_db_table_naughtystring)
cursor.execute(create_db_table_naughty_usernames)
cursor.execute(create_db_table_naughty_password)

# http headers
def prepare_http_headers():
    nsgen = NaughtyHttpHeadersGenerator(cursor)
    df =  nsgen.generate_httpheaders()
    print('http headers completed')


            
def prepare_useragentstring():
    nsgen = NaughtyUserAgentGenerator(cursor)
    df =  nsgen.generate_useragents()
    print('user agents completed')

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

# strings
def prepare_naughty_string():
    nsgen = NaughtyStringGenerator(cursor)
    nsgen.generate_naughty_strings()
    print('naughty string completed')

def prepare_naughty_username():
    generator = NaughtyUsernameGenerator(cursor)
    generator.generate_naughty_usernames()
    print('naughty username completed')

def prepare_naughty_password():
    generator = NaughtyPasswordGenerator(cursor)
    generator.generate_naughty_password()
    print('naughty password completed')

def removeDoubleQuotes(content: str):
    r = content.replace('"', '')
    return r

if __name__ == '__main__':
    # prepare_useragentstring()
    # prepare_http_headers()
    # prepare_naughty_files()
    # prepare_naughty_string()
    
    #prepare_naughty_username()
    prepare_naughty_password()
    sqliteconn.close()
    
    print("data loading completed")


