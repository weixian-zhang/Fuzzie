import sqlite3
from storagemanager import StorageManager
import base64
import os, sys
import io
from pathlib import Path
import requests
from io import BytesIO

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
from fpdf import FPDF, HTMLMixin
import datetime
import jinja2
import json
import hashlib
import zlib

class CustomFPDF(FPDF, HTMLMixin):
    pass

# create tables if not exist
metadata.create_all()

dbpath = os.getcwd() + "\src\core\core\corporafactory\data\\fuzzie.sqlite"

sqliteconn = sqlite3.connect(dbpath, isolation_level=None)

cursor = sqliteconn.cursor()

encoding = 'utf-8'
sm = StorageManager()

def shortenStr(text: str, length=20):
    if len(text) > length:
        newText = text[:(length-1)]
        return newText + '...'
    else:
        return text
    
def load_pdf():
    
    try:
        
        faker = Faker()
        
        
        for _ in range(1000):
            
            html = '''
            <html>
                <body>
                    <H1 align="center">Fuzzie Report - User Info</H1>
                    <p>{{ datetime }}</p>
                    <table border="1" align="center" width="100%" style="table-layout: fixed;">
                        <thead>
                            <tr>
                                <th width="40%">
                                Name
                                </th>
                                <th width="60%">
                                Address
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {%- for item in info %}
                                <tr>
                                    <td>
                                        {{ item['name'] }}
                                    </td>
                                    <td>
                                        {{ item['address'] }}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </body>
            </html>
            '''
            
            info = []
            
            for _ in range(10):
                info.append({
                    'name': faker.name(),
                    'address': shortenStr(faker.address()),
                    'job': shortenStr(faker.job()),
                })
                
            
            jinjaTpl = jinja2.Template(html)
            output = jinjaTpl.render({
                'info': info,
                'datetime': datetime.datetime.now()
                })
       
            pdf = CustomFPDF()
            pdf.add_page()
            pdf.author = 'Fuzzie'
            
            pdf.write_html(output)
            
            htmlStr = pdf.output(dest='S').decode('latin-1')
            
            htmlBackToBytes = bytes(htmlStr, encoding='latin-1')   
        
            b64 = base64.b64encode(htmlBackToBytes).decode('latin-1')    # to remove b prefix
            
            cursor.execute(f'''
                    insert into SeclistPDF (Content)
                    values ("{b64}")
                    ''')
        
    except Exception as e:
        print(f'''{e}''')

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


def load_image():
    
    #https://medium.com/apis-with-valentine/how-to-use-the-dall-e-2-api-from-openai-to-generate-images-in-postman-687aa5419e77
    prompts = [
                'Segmented concentric arcs and circles of varying thicknesses (artificial geometric designs)',
                'Egyptian art',
                'Cobras (aka uraeus)',
                'Sun disks',
                'Gold jewelry',
                'Diamonds and jewels',
                'Thick, heavy eyeliner (kohl)',
                'Pyramids',
                'Gods (deity)',
                'Temple pylon gates',
                'Mummies',
                'Camels',
                'Sand',
                'Palm trees',
                'Papyrus reeds',
                'Egyptian hieroglyphics',
                'Ushabti',
                'Blue scarabs',
                'Cats, especially black ones',
                'Nefertiti headdress',
                'Cleopatra hairstyle (shoulder length straight black hair with thick bangs)',
                'Black outfits with neon accent colors',
                'Lab or trench coats',
                'Futuristic glasses, eyewear, or masks',
                'Body modifications',
                'Cargo pants',
                'Belts, buckles and pockets',
                'Leather jackets',
                'Jacket patches (usually ‘edgy’ in nature)',
                'Tattoos',
                'Bandanas',
                'Black',
                'Bike helmets',
                'jeans/ripped jeans',
                'Leather vests',
                'Beards',
                'Finger-less gloves',
                'Drinking/eating',
                'Swimming',
                'Building sand-castles',
                'Tanning',
                'Watching the sunset',
                'Playing games (ex.cards)',
                'Gears',
                'Roman Numerals',
                'Numbers',
                'Vintage Clocks',
                'Clockwork of any kind',
                'Padlocks',
                'Pocket Watches',
                'Breakfast foods such as pancakes and eggs',
                'Burgers and French fries',
                'Booths',
                'Checkered floors',
                'Chrome counters',
                'Coca-cola, and specifically this brand',
                'Ice cream sundaes',
                'Jukeboxes',
                'Napkin dispensers',
                'Milkshakes',
                'Mugs of coffee',
                'Neon signs',
                'Photographs of famous people visiting the establishment, newspaper clippings, advertisements, etc.',
                'Pie',
                'Roller skates',
                'Toadstools',
                'Shelf mushrooms',
                'Fairy rings (Mushroom circles)',
                'Forest',
                'Moist, muddy soil, mud',
                'Dried leaves',
                'Stones',
                'Insects',
                'Frogs, slugs, and snails',
                'Gnomes',
                'Nature spirits',
                'Moss',
                'Dead logs',
                'Oversized objects',
                'Large patterns',
                'Handmade things',
                'Things that many people consider trash',
                'earth after human extinction, a new beginning, nature taking back the planet, harmony, peace, earth balanced --version 3 --s 42000 --uplight --ar 4:3 --no text, blur, people, humans, pollution',
                'earth reviving after human extinction, a new beginning, nature taking over buildings, animal kingdom, harmony, peace, earth balanced --version 3 --s 1250 --uplight --ar 4:3 --no text, blur',
                'Freeform ferrofluids, beautiful dark chaos, swirling black frequency --ar 3:4 --iw 9 --q 2 --s 1250',
                'a home built in a huge Soap bubble, windows, doors, porches, awnings, middle of SPACE, cyberpunk lights, Hyper Detail, 8K, HD, Octane Rendering, Unreal Engine, V-Ray, full hd -- s5000 --uplight --q 3 --stop 80--w 0.5 --ar 1:3',
                'photo of an extremely cute alien fish swimming an alien habitable underwater planet, coral reefs, dream-like atmosphere, water, plants, peaceful, serenity, calm ocean, tansparent water, reefs, fish, coral, inner peace, awareness, silence, nature, evolution --version 3 --s 42000 --uplight --ar 4:3 --no text, blur',
                'rubber duck duke ellington. Harlem jazz club. Singing. Mic. Ambience',
                'surreal blueish monk, dodecahedron for his head, amazing details, hyperrealistic photograph, octane made of billions of intricate small houses, GODLIKE, bokeh, photography on mars, cinematic lighting, --ar 9:21',
                '2 medieval warriors ::0.4 travelling on a cliff to a background castle , view of a coast line landscape , English coastline, Irish coastline, scottish coastline, perspective, folklore, King Arthur, Lord of the Rings, Game of Thrones. Photographic, Photography, photorealistic, concept art, Artstation trending , cinematic lighting, cinematic composition, rule of thirds , ultra-detailed, dusk sky , low contrast, natural lighting, fog, realistic, light fogged, detailed, atmosphere hyperrealistic , volumetric light, ultra photoreal, | 35mm| , Matte painting, movie concept art, hyper-detailed, insanely detailed, corona render, octane render, 8k, --ar 3:1 --no blur',
                'hyerophant, god light, cinematic look, octane render, under water, --wallpaper',
                'modern kids play area landscape architecture, water play area, floating kids, seating areas, perspective view, rainy weather, biopunk, cinematic photo, highly detailed, cinematic lighting, ultra-detailed, ultrarealistic, photorealism, 8k, octane render, --ar 16:12'
              ]
    size = ['256x256','512x512']    #, '1024x1024'

    randSizeIdx = random.randint(0,1)
    
    for p in prompts:

        resp = requests.post('https://api.openai.com/v1/images/generations',
                    headers= {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer '
                    },
                    json={
                        "prompt": p,
                        "n": 2,
                        "size": size[randSizeIdx]
                    })
        
        jObj = json.loads(resp.text)
        imgUrls = jObj['data']
        
        for u in imgUrls:
            
            url = u['url']
            
            response = requests.get(url)
            
            b64Str = base64.b64encode(response.content).decode('latin-1')
            
            #save to file for testing
            # with open("C:\\Users\\weixzha\\Desktop\\dalle\\{filename + '.png'}", "wb") as fh:
            #     fh.write(base64.b64decode(b64Str))
            
            cursor.execute(f'''
                insert into RandomImage (Content)
                values ("{ b64Str }")
                ''')
            
            pass
            
            
    # content = sm.download_file_as_bytes(fp)
            
    # decodedStr = Utils.try_decode_bytes_string(content)
    
    # b64Bytes = base64.b64encode(bytes(decodedStr, encoding='UTF-8'))
    
    # b64Str = Utils.try_decode_bytes_string(b64Bytes)
    
    # cursor.execute(f'''
    #     insert into SeclistPayload (Filename, Content)
    #     values ("{os.path.basename(fp)}", "{b64Str}")
    #     ''')

# def load_image(size=300):
#     imgSize = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,
#                         450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,825,850,875,900,925,950,975,1000]
#     colors = ['0000FF', '808080', 'FF0000','008000', 'FFFFF']
#     ext = ['.png', '.gif', '.jpg' '.jpeg']
#     faker = Faker()
#     http = urllib3.PoolManager()
    
#     for i in range(size):
            
#             randSizeW = imgSize[random.randint(0, len(imgSize) - 1)]
#             randSizeH = imgSize[random.randint(0, len(imgSize) - 1)]
#             randColor = colors[random.randint(0, len(colors) - 1)]
#             randExt = ext[random.randint(0, len(ext) - 1)]
#             texte = urllib.parse.quote_plus(faker.name())
#             url = f'https://via.placeholder.com/{randSizeW}x{randSizeH}{randExt}?text={texte}'
            
#             r = http.request('GET', url)
#             imgByte = r.data
#             imgStr = base64.b64encode(imgByte)
            
#             cursor.execute(f'''
#                     insert into RandomImage (Content)
#                     values ("{imgStr}")
#                     ''')
        
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
    
    # load_pdf()
    
    load_image()
    
    # load_seclist_char()
    
    #load_seclist_payload()
    
    # load_seclist_string()
    
    #load_seclist_username()
    
    #load_seclist_password()
    
    #load_seclist_xss()
    
    #load_seclist_sqlinjection()

    sqliteconn.close()
    
    print("data loading completed")


