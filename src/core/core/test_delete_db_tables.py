import os, sys
from pathlib import Path
datafacPath = os.path.join(os.path.dirname(Path(__file__)), 'datafactory')
dbPath = os.path.join(os.path.dirname(Path(__file__)), 'datafactory/data')
modelsPath = os.path.join(os.path.dirname(Path(__file__)), 'models')
sys.path.insert(0, datafacPath)
sys.path.insert(0, dbPath)
sys.path.insert(0, modelsPath)

from db import metadata
metadata.drop_all()