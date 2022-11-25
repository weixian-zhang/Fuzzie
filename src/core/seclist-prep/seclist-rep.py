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

dbpath = os.getcwd() + "\src\core\core\corporafactory\data\\fuzzie.sqlite"

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
charPath = os.path.join(dataPath, 'seclist', 'char')

# chars
def load_seclist_char():
    
        ffPath = os.path.join(charPath, 'chars-final.txt')
            
        f = io.open(ffPath, mode="r", encoding="utf-8")
        content = f.readlines()
        
        for ns in content:        
            
            ns = ns.replace('"', '')
            ns = ns.replace('\n', '')
            ns = ns.replace('\r\n', '')
            
            if ns == '':
                continue
            
            cursor.execute(f'''
                    insert into SeclistChar (Content)
                    values ("{ns}")
                    ''')
           
                
        print('seclist char completed')

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
                        insert into SeclistXSS (Content)
                        values ("{ns}")
                        ''')
    print('seclist xss completed')
    
def load_seclist_sqlinjection():
    
    try:
        for dirpath, _, filenames in os.walk(sqlinjPath):
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
                            insert into SeclistSqlInjection (Content)
                            values ("{ns}")
                            ''')
        print('seclist sql injection completed')
        
    except Exception as e:
        print(f'file:{ffPath}, error: {e}')


    

def removeDoubleQuotes(content: str):
    r = content.replace('"', '')
    return r

if __name__ == '__main__':
    
    load_seclist_char()
    
    #load_seclist_payload()
    
    load_seclist_string()
    
    #load_seclist_username()
    
    #load_seclist_password()
    
    #load_seclist_xss()
    
    #load_seclist_sqlinjection()

    sqliteconn.close()
    
    print("data loading completed")


