 from setuptools import setup

 setup(
   name='RedHouse',
   version='0.1.0',
   author='Dave Fugelso',
   author_email='aac@example.com',
   packages=['RedHouse', 'RedHouse.test'],
   scripts=['bin/script1','bin/script2'],
   url='http://pypi.python.org/pypi/RedHouse/',
   license='LICENSE.txt',
   description='This is the RedHouse client package',
   long_description=open('README.txt').read(),
   install_requires=[
       "pytest",
   ],
)