from setuptools import setup
import codecs
from os import path

def read(rel_path):
    here = path.abspath(path.dirname(__file__))
    with codecs.open(path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

# Get the long description from the relevant files
readme = read('README.md')
changelog = read('CHANGELOG.md')
desc = readme + '\n\n' + changelog

setup(
      name="ntfit",
      version=get_version("ntfit/__init__.py"),
      description="nonuniform-temperature fitting",
      url="https://gitlab.com/nam5312/ntfit",
      author="Nathan Malarich",
      author_email="nathan.malarich@colorado.edu",
      packages=['ntfit','ntfit.hapi','ntfit.spectrafit'],
      install_requires=[ # combustion-custom Hapi included in package
          "numpy", # standard math/arrays, also numpy.linalg.norm and numpy.matlib.repmat
          "matplotlib",
          "scipy", # for nonlinear least-squares fitting
      ],
      long_description = desc,
      long_description_content_type = 'text/markdown',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: Microsoft :: Windows :: Windows 10',      
        'Programming Language :: Python :: 3.6',
    ],
)