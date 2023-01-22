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

from faker import Faker
import random
import urllib.parse
import urllib3
from faker import Faker
import base64
from utils import Utils
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
    
    try:
        for fp in fileNamePaths:
            
            content = sm.download_file_as_bytes(fp)
            
            decodedStr = Utils.try_decode_bytes_string(content)
            
            b64Bytes = base64.b64encode(bytes(decodedStr, encoding='UTF-8'))
            
            b64Str = Utils.try_decode_bytes_string(b64Bytes)
            
            cursor.execute(f'''
                insert into SeclistPayload (Filename, Content)
                values ("{os.path.basename(fp)}", "{b64Str}")
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

def load_image(size=300):
    imgSize = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,
                        450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,825,850,875,900,925,950,975,1000]
    colors = ['0000FF', '808080', 'FF0000','008000', 'FFFFF']
    ext = ['.png', '.gif', '.jpg' '.jpeg']
    faker = Faker()
    http = urllib3.PoolManager()
    
    for i in range(size):
            
            randSizeW = imgSize[random.randint(0, len(imgSize) - 1)]
            randSizeH = imgSize[random.randint(0, len(imgSize) - 1)]
            randColor = colors[random.randint(0, len(colors) - 1)]
            randExt = ext[random.randint(0, len(ext) - 1)]
            texte = urllib.parse.quote_plus(faker.name())
            url = f'https://via.placeholder.com/{randSizeW}x{randSizeH}{randExt}?text={texte}'
            
            r = http.request('GET', url)
            imgByte = r.data
            imgStr = base64.b64encode(imgByte)
            
            cursor.execute(f'''
                    insert into RandomImage (Content)
                    values ("{imgStr}")
                    ''')
        
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
    
    # load_image()
    
    # load_seclist_char()
    
    load_seclist_payload()
    
    # load_seclist_string()
    
    #load_seclist_username()
    
    #load_seclist_password()
    
    #load_seclist_xss()
    
    #load_seclist_sqlinjection()

    sqliteconn.close()
    
    print("data loading completed")


