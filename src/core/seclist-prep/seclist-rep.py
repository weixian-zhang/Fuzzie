from naughty_file_generator import NaughtyFilesGenerator
from naughty_string_generator import NaughtyStringGenerator
from naughty_username_generator import NaughtyUsernameGenerator
from naughty_password_generator import NaughtyPasswordGenerator
from naughty_useragent_generator import NaughtyUserAgentGenerator
from naughty_httpheaders_generators import NaughtyHttpHeadersGenerator
import pandas as pd
import sqlite3
from storagemanager import StorageManager
import base64
import os, sys
import io
from pathlib import Path
dbModulePath = os.path.join(os.path.dirname(Path(__file__).parent), 'core')
modelPath = os.path.join(os.path.dirname(Path(__file__).parent), 'core', 'models')
sys.path.insert(0, dbModulePath)
sys.path.insert(0, modelPath)

from db import metadata

# create tables if not exist
metadata.create_all()


# files with metadata isLongFileName has no content but with very long file name to break systems that cannot
# handle very long file names
# exclude zipbombs
# create_db_table_naughtyfile = '''
# CREATE TABLE IF NOT EXISTS NaughtyFile (
#     id integer PRIMARY KEY AUTOINCREMENT,
# 	Filename TEXT NOT NULL,
# 	Content TEXT NOT NULL,
#     RowNumber integer NOT NULL
# );
# '''


# create_db_table_naughtyuseragent= '''
# CREATE TABLE IF NOT EXISTS NaughtyUserAgent (
#     id integer PRIMARY KEY AUTOINCREMENT,
#     Content TEXT NOT NULL,
#     RowNumber integer NOT NULL
# );

# '''

# create_db_table_naughtystring = '''
# CREATE TABLE IF NOT EXISTS NaughtyString (
#     id integer PRIMARY KEY AUTOINCREMENT,
#     Content TEXT NOT NULL,
#     RowNumber integer NOT NULL
# );

# '''

# create_db_table_naughty_usernames = '''
# CREATE TABLE IF NOT EXISTS NaughtyUsername (
#     id integer PRIMARY KEY AUTOINCREMENT,
#     Content TEXT NOT NULL,
#     RowNumber integer NOT NULL
# );
# '''

# create_db_table_naughty_password= '''
# CREATE TABLE IF NOT EXISTS NaughtyPassword (
#     id integer PRIMARY KEY AUTOINCREMENT,
#     Content TEXT NOT NULL,
#     RowNumber integer NOT NULL
# );
# '''

dbpath = os.getcwd() + "\src\core\core\datafactory\data\\fuzzie.sqlite"

sqliteconn = sqlite3.connect(dbpath, isolation_level=None)

cursor = sqliteconn.cursor()

encoding = 'utf-8'
sm = StorageManager()

#*** prepare naughty files
def load_seclist_payload():
    
    fileNamePaths = sm.get_file_names_of_directory('daniel-seclist/payload')
        
    if len(fileNamePaths.items) == 0:
        return []
    
    df = pd.DataFrame()
    
    try:
        for fp in fileNamePaths:
            
            content = sm.download_file_as_bytes(fp)
            b64e = base64.b64encode(content)
            
            cursor.execute(f'''
                insert into SeclistPayload (Filename, Content)
                values ("{os.path.basename(fp)}", "{b64e}")
                ''')
        
        print('seclist payload completed')
    except Exception as e:
        print(f'''file:{fp}, {e}''')
    

dataPath = os.path.join(os.path.dirname(Path(__file__)), 'data')
blnsPath = os.path.join(dataPath, 'seclist', 'naughty-string')
usernamePath = os.path.join(dataPath, 'seclist', 'username')
passwordPath = os.path.join(dataPath, 'seclist', 'password')
sqlinjPath = os.path.join(dataPath, 'seclist', 'sql-injection')
xssPath = os.path.join(dataPath, 'seclist', 'xss')

# strings
def load_seclist_string():
    
    for dirpath, _, filenames in os.walk(blnsPath):
        for filename in filenames:
            ffPath = os.path.join(dirpath, filename)
            
            f = io.open(ffPath, mode="r", encoding="utf-8")
            content = f.readlines()
            
            for ns in content:        
                
                if ns.startswith('#'):
                    continue
                
                ns = ns.replace('"', '')
                ns = ns.replace('\n', '')
                ns = ns.replace('\r\n', '')
                
                if ns == '':
                    continue
                
                cursor.execute(f'''
                        insert into SeclistBLNS (Content)
                        values ("{ns}")
                        ''')
                
    print('seclist blns completed')
        

def load_seclist_username():
    
    for dirpath, _, filenames in os.walk(usernamePath):
        for filename in filenames:
            ffPath = os.path.join(dirpath, filename)
            
            f = io.open(ffPath, mode="r", encoding="utf-8")
            content = f.readlines()
            
            for ns in content:        
                
                ns = ns.replace('"', '')
                ns = ns.replace('\n', '')
                ns = ns.replace('\r\n', '')
                
                if ns == '':
                    continue
                
                cursor.execute(f'''
                        insert into SeclistUsername (Content)
                        values ("{ns}")
                        ''')
    print('seclist username completed')

def load_seclist_password():
    for dirpath, _, filenames in os.walk(passwordPath):
        for filename in filenames:
            ffPath = os.path.join(dirpath, filename)
            
            f = io.open(ffPath, mode="r", encoding="utf-8")
            content = f.readlines()
            
            for ns in content:        
                
                ns = ns.replace('"', '')
                ns = ns.replace('\n', '')
                ns = ns.replace('\r\n', '')
                
                if ns == '':
                    continue
                
                cursor.execute(f'''
                        insert into SeclistPassword (Content)
                        values ("{ns}")
                        ''')
    print('seclist password completed')
    
def load_seclist_xss():
    for dirpath, _, filenames in os.walk(xssPath):
        for filename in filenames:
            ffPath = os.path.join(dirpath, filename)
            
            f = io.open(ffPath, mode="r", encoding="utf-8")
            content = f.readlines()
            
            for ns in content:        
                
                ns = ns.replace('"', '')
                ns = ns.replace('\n', '')
                ns = ns.replace('\r\n', '')
                
                if ns == '':
                    continue
                
                cursor.execute(f'''
                        insert into SeclistPassword (Content)
                        values ("{ns}")
                        ''')
    print('seclist xss completed')
    
def load_seclist_sqlinjection():
    for dirpath, _, filenames in os.walk(sqlinjPath):
        for filename in filenames:
            ffPath = os.path.join(dirpath, filename)
            
            f = io.open(ffPath, mode="r", encoding="utf-8")
            content = f.readlines()
            
            for ns in content:        
                
                ns = ns.replace('"', '')
                ns = ns.replace('\n', '')
                ns = ns.replace('\r\n', '')
                
                if ns == '':
                    continue
                
                cursor.execute(f'''
                        insert into SeclistPassword (Content)
                        values ("{ns}")
                        ''')
    print('seclist sql injection completed')

def removeDoubleQuotes(content: str):
    r = content.replace('"', '')
    return r

if __name__ == '__main__':
    
    #load_seclist_payload()
    
    #load_seclist_string()
    
    #load_seclist_username()
    
    load_seclist_password()
    
    load_seclist_xss()
    
    load_seclist_sqlinjection()
    
    # prepare_useragentstring()
    # prepare_http_headers()
    # prepare_naughty_files()
    # prepare_naughty_string()
    

    sqliteconn.close()
    
    print("data loading completed")


