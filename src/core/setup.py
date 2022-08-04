from codecs import ignore_errors
from dataclasses import replace
from setuptools import setup, find_packages
import os

with open('requirements.txt', 'rb') as f:
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
   packages=find_packages(),  #same as name
   install_requires=required, #external packages as dependencies
   scripts=[]
)