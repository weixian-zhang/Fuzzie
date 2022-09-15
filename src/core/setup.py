

from setuptools import setup, find_packages

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
   data_files=["data/*"],     #contains sqlite.db and other data files
   packages=find_packages(),  #same as name
   install_requires=required  #external packages as dependencies
)