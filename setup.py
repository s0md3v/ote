#!/usr/bin/env python3

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

setup(
    name='ote',
    version='0.0.3',
    description='CLI application to generate emails and fetch OTPs',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/s0md3v/ote',
    download_url='https://github.com/s0md3v/ote/releases',
    author='Somdev Sangwan',
    author_email='s0md3v@gmail.com',
    maintainer='Somdev Sangwan',
    maintainer_email='s0md3v@gmail.com',
    install_requires=['requests','html2text'],
    packages=['ote'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'ote = ote.__main__:main'
        ]
    },
)
