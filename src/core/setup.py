from setuptools import setup, find_packages

from pathlib import Path
import os

curDir = os.path.dirname(Path(__file__))
requirementTxtPath = os.path.join(curDir, 'core', 'requirements.txt')

required_modules = []

with open(requirementTxtPath, 'rb') as f:
    decode = f.read().decode("utf-8")
    
    splitted = decode.split('\r\n')
    for fn in splitted:
        required_modules.append(fn)
    
setup(
   name='Fuzzie',
   description='',
   license="MIT",
   author='WXZ',
   packages=find_packages(
       exclude=[
           "tests",
           "seclist-prep",
           "build",
           "dist",
           ".git",
           ".gitignore",
           "Fuzzie.egg-info",
           "requirements.txt",
           "core/core/api_discovery/testdata",
           "core/core/corporafactory/test_*",
           "core/core/.env"
           ]
       
    ),  #same as name
   install_requires=required_modules #required  #external packages as dependencies
   
)