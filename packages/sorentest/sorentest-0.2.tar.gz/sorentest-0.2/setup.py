try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'sorentest',         # How you named your package folder (MyLib)
  packages = ['sorentest'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package to test pypi, github actions and other automations',   # Give a short description about your library
  author = 'Søren Bertelsen',                   # Type in your name
  author_email = 'sorenbertelsen@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/sqbl/SorenTest',   # Provide either the link to your github or to your website
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',          
      ],
  extras_require={
          "add1": ['matplotlib'],
          "add2": ['matplotlib', 'numpy==1.23.1']
          },
  )
