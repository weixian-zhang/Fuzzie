

from setuptools import setup, find_packages
import os

sqlitedb = os.getcwd() + "\core\corporafactory\data\\fuzzie.sqlite"
# localhost_crt = os.getcwd() + "\core\certs\localhost+2.pem"
# localhost_key= os.getcwd() + "\core\certs\localhost+2-key.pem"

with open('core/requirements.txt', 'rb') as f:
    required = f.read()
    required = required.decode("utf-16")
    print(required)
    
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
   packages=find_packages(),  #same as name
   install_requires=required  #external packages as dependencies
)



    