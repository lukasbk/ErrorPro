import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "errorpypagation",
    version = "0.0.1",
    author = "Lukas Bentkamp",
    author_email = "",
    description = ("calculates physical quantities from data including units and uncertainty propagation."),
    license = "BSD",
    keywords = "error uncertainty propagation units physics",
    url = "http://github.com/lukasbentkamp/Error-Pypagation",
    packages=['errorpypagation'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: BSD License",
    ],
)
