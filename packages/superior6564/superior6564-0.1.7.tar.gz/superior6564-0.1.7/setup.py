#!/usr/bin/env python

from io import open
from setuptools import setup
import requests


"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""


# version = '0.1.5'

with open('README.md') as f:
    previous_version = f.readline()[22:].strip()
    if int(previous_version[4]) < 9:
        previous_num = previous_version[4]
        new_num = str(int(previous_version[4]) + 1)
        new_version = previous_version[:-1] + new_num
    elif int(previous_version[2]) < 9:
        previous_num = previous_version[2]
        new_num = str(int(previous_version[2]) + 1)
        new_version = previous_version[0:2] + new_num + ".0"
    elif int(previous_version[0]) < 9:
        previous_num = previous_version[0]
        new_num = str(int(previous_version[0]) + 1)
        new_version = new_num + previous_version[1:]
    test_description = f.read()

# version = '0.1.5'
version = new_version

with open('README.md', "w") as f:
    install_description = "Version of package is " + version + "\n" + test_description
    f.write(install_description)

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='superior6564',
    version=version,

    author='Superior_6564',
    author_email='vip.klochayil@gmail.com',

    description=(
        u'Python library which maybe will help to people. '
        u'Before using you need to run packages.required()'
    ),
    long_description=long_description,
    # long_description_content_type='text/markdown',

    url='https://github.com/Superior-GitHub/Superior6564',
    download_url='https://github.com/Superior-GitHub/Superior6564/archive/refs/heads/main.zip'.format(version),

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['superior6564'],
    install_requires=['', ''],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
