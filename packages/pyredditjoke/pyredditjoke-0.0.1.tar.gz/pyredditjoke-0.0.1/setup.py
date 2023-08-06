from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 2 - Pre-Alpha',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyredditjoke',
  version='0.0.1',
  description='Download reddit jokes',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Kevin Wirtz',
  author_email='kevin.wirtz@unistra.fr',
  license='MIT', 
  classifiers=classifiers,
  keywords='jokes', 
  packages=find_packages(),
  install_requires=['pymongo','selenium'] 
)