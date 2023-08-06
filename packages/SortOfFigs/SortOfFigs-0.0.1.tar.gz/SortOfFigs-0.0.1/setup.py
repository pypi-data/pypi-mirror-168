from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'PythonProgram'
LONG_DESCRIPTION = 'A package for sortint of different figures'

# Setting up
setup(
    name="SortOfFigs",
    version=VERSION,
    author="Gopal Tiwari",
    author_email="gopaltiwarigopal786@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tutorial', 'area of figs', 'area', 'developergautam'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)