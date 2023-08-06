from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ethan-refinary-extractor',
  version='0.0.1',
  description='Extration methods for complex type of statements',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Nandi Prasad Madikeri',
  author_email='nandi@ethan-ai.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Extractor', 
  packages=find_packages(),
  install_requires=[''] 
)
