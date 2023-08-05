from setuptools import setup, find_packages

version = '0.0.6'



base_packages = ['networkx','pyvis','leidenalg','autocorrect','coreferee','spacy<3.5.0,>=3.0.0','autocorrect','xlsxwriter','igraph','matplotlib','numpy']
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='keypartx',
  version=version,
  description='A Graph-based Perception(Text) Representation',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Peng Yang',
  author_email='pyseptimo@outlook.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['text representation','text mining','nlp'], 
  packages=find_packages(),
  install_requires= base_packages
)


