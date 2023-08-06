from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  "Intended Audience :: Developers",
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ColorCraft',
  version='0.3.0',
  description='simplest and coolest color Library. print and menaged colors in Python!',
  long_description=open('README.md').read() + "\n\n" + open("whats_new.md").read() + "\n" +'\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Alawi Hussein Adnan Al Sayegh',
  author_email='programming.laboratorys@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ColorCraft', 
  packages=find_packages(),
  install_requires=[''] 
)
