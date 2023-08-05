from setuptools import setup, find_packages
import codecs
import os

VERSION = '8.1'
DESCRIPTION = 'A Minecraft schematic creator library.'
LONG_DESCRIPTION = 'Allows the creation of Minecraft schematic files directly through code. And soon the editing of schematics saved on drives too!'

with open("README.md", "r") as readme:
    LONG_DESCRIPTION = readme.read()

# Setting up
setup(
    name="mcschematic",
    version=VERSION,
    author="Sloimay",
    author_email="<sloimayyy@gmail.com>",
    license="Apache License 2.0",
    description=DESCRIPTION,
    
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    
    packages=find_packages(),
    install_requires=['nbtlib'],
    readme="README.md",
    keywords=['python', 'minecraft', 'schematic'],
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)