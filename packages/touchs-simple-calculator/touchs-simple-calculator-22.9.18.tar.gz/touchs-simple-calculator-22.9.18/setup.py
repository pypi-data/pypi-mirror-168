from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 7 - Inactive',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='touchs-simple-calculator',
  version='22.9.18',
  description='A simple calculator library made with the tutorial from Joshua Lowe.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/Touchcreator/Simple-Calculator',  
  author='Touchcreator',
  author_email='touchgamer95@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[''] 
)