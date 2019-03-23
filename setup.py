#!/usr/bin/env python3
from codecs import open
from os import path
from setuptools import find_packages, setup

root = path.abspath(path.dirname(__file__))
with open(path.join(root, 'README.md'), encoding='utf-8') as f:
    long_desc = f.read()
setup(
    name='earthpy',
    version='0.0.1',
    description='Download and process Earth data',
    long_description='long_desc',
    long_description_content_type='text/markdown',
    url='https://github.com/138paulmiller/earthpy',
    author='138paul',
    classifiers=[
        'Topic :: Scientific/Engineering :: GIS',
        'Programming Language :: Python :: 3',
    ],
    keywords=['gis', 'earth tiles','srtm', 'satellite imagery'],
    install_requires=['numpy', 'scikit-image', 'argparse', 'matplotlib'],
    zip_safe=False,
    entry_points='''
        [console_scripts]
        earthpy=earthpy.cli:cli
        '''    
    )

