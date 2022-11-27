from faker import Faker
import random
import urllib.parse
import urllib3
from string_corpora import StringCorpora

class ImageCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ImageCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:

        self.data = []
        
        self.faker = Faker()
        
        self.strCorpora = StringCorpora()
        self.strCorpora.load_corpora()
        
        self.http = http = urllib3.PoolManager()
        
        self.imgSize = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,
                        450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,825,850,875,900,925,950,975,1000]
        self.colors = ['0000FF', '808080', 'FF0000','008000', 'FFFFF']
        self.ext = ['.png'] #'.gif', '.jpg' '.jpeg', 
        
    def load_corpora(self, size=500):
        
        for i in range(size):
            
            randSizeW = self.imgSize[random.randint(0, len(self.imgSize) - 1)]
            randSizeH = self.imgSize[random.randint(0, len(self.imgSize) - 1)]
            randColor = self.colors[random.randint(0, len(self.colors) - 1)]
            randExt = self.ext[random.randint(0, len(self.ext) - 1)]
            texte = urllib.parse.quote_plus(self.faker.name())
            url = f'https://via.placeholder.com/{randSizeW}x{randSizeH}{randExt}?text={texte}'
            
            
            r = self.http.request('GET', url)
            imgByte = r.data
            
            self.data.append(imgByte)
    
    def next_corpora(self):
        
        randIdx = random.randint(0, len(self.data) - 1)
        return self.data[randIdx]
    