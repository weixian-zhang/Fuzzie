from setuptools import setup, find_packages

from pathlib import Path
import os

sqlitedb = os.getcwd() + "\core\corporafactory\data\\fuzzie.sqlite"
# localhost_crt = os.getcwd() + "\core\certs\localhost+2.pem"
# localhost_key= os.getcwd() + "\core\certs\localhost+2-key.pem"

curDir = os.path.dirname(Path(__file__))
requirementTxtPath = os.path.join(curDir, 'core', 'requirements.txt')

required_modules = []
modules_to_exclude = ['pyinstaller==5.1', 'pyinstaller-hooks-contrib', 'pylint']

with open(requirementTxtPath, 'rb') as f:
    decode = f.read().decode("utf-8")
    
    splitted = decode.split('\r\n')
    for fn in splitted:
        if fn not in modules_to_exclude:
            required_modules.append(fn)
    
setup(
   name='Fuzzie',
   version='1.0',
   description='',
   license="MIT",
   long_description='',
   author='Man Foo',
   author_email='',
   url="",
   data_files=[sqlitedb], #, localhost_crt, localhost_key],     #contains sqlite.db and other data files
   packages=find_packages(
       exclude=[
           "tests",
           "build",
           "dist",
           ".git",
           ".gitignore",
           "Fuzzie.egg-info",
           "__pycache__"
           ]
       
    ),  #same as name
   install_requires=required_modules #required  #external packages as dependencies
   
)