import setuptools
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='statts',
  version='1.2',
  description="A library for all statistical operations",
  long_description=open('README.md').read(),
  url='',  
  author='Pranendu Bikash Pradhan',
  author_email='b219040@iiit-bh.ac.in',
  license='MIT', 
  classifiers=classifiers,
  keywords='stats statistics maths', 
  packages=['statts'],
  install_requires=[''] 
)