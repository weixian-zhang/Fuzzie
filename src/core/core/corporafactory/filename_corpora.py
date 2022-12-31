import os, sys
from pathlib import Path
currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)

import string
import random
import uuid
import datetime

class FileNameCorpora:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileNameCorpora, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        
        self.imageExtensions = [
            '.jpg',
            '.png',
            '.gif',
            '.webp',
            '.tiff',
            '.psd',
            '.raw',
            '.bmp',
            '.heif',
            '.indd',
            '.jpeg',
            '.svg',
            '.ai',
            '.eps',
        ]
        
        self.extensions = ['7z',
                            'asmx',
                            'asp',
                            'aspx',
                            'bak',
                            'bat',
                            'bin',
                            'bz2',
                            'c',
                            'cc',
                            'cfg',
                            'cfm',
                            'cgi',
                            'class',
                            'cnf',
                            'conf',
                            'config',
                            'cpp',
                            'cs',
                            'csv',
                            'dat',
                            'db',
                            'dll',
                            'do',
                            'doc',
                            'dump',
                            'ep',
                            'err',
                            'error',
                            'exe',
                            'gif',
                            'gz',
                            'htm',
                            'html',
                            'inc',
                            'ini',
                            'java',
                            'jhtml',
                            'jpg',
                            'js',
                            'jsf',
                            'jsp',
                            'key',
                            'lib',
                            'log',
                            'lst',
                            'manifest',
                            'mdb',
                            'meta',
                            'msg',
                            'nsf',
                            'o',
                            'old',
                            'ora',
                            'orig',
                            'out',
                            'part',
                            'pdf',
                            'php',
                            'php3',
                            'phtml',
                            'pl',
                            'pm',
                            'png',
                            'ppt',
                            'properties',
                            'py',
                            'rar',
                            'rss',
                            'rtf',
                            'save',
                            'sh',
                            'shtml',
                            'so',
                            'sql',
                            'stackdump',
                            'swf',
                            'tar',
                            'tar.bz2',
                            'tar.gz',
                            'temp',
                            'test',
                            'tgz',
                            'tmp',
                            'trace',
                            'txt',
                            'vb',
                            'vbs',
                            'ws',
                            'xls',
                            'xml',
                            'xsl',
                            'zip',
]
        self.data = {}
        
        self.rowPointer = 1; #important as sqlitre autoincrement id starts from 1
        
        # lowerLetter = string.ascii_lowercase
        # upperLetters = string.ascii_uppercase
        # hexs = string.hexdigits
        # punctuations = string.punctuation
        # letters = string.ascii_lowercase

    
    def load_corpora(self):
        pass
        
    def next_corpora(self, fileType='file'):
        
        ext = 'pdf' #set a default, no particular reason for pdf
        
        basename = str(uuid.uuid4())[:random.randint(0, 256)]    # more than 255 chars
        
        randY = random.randint(1970, 2022)
        randMth = random.randint(1, 12)
        randDay = random.randint(1, 28)
        randHr = random.randint(1, 23)
        randMin = random.randint(1, 59)
        randSec = random.randint(1, 59)
        
        suffix = datetime.datetime(randY, randMth, randDay, randHr, randMin, randSec).strftime("%y%m%d_%H%M%S")
        
        if fileType == 'file':
            extIndex =  random.randint(0, len(self.extensions) - 1)
            ext = self.extensions[extIndex]
        elif fileType == 'image':
            extIndex =  random.randint(0, len(self.imageExtensions) - 1)
            ext = self.imageExtensions[extIndex]
            
        fn = f'{basename}_{suffix}.{ext}'
        
        return fn
        
        