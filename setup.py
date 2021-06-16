#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from codecs import open

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='normalize-japanese-address',
        packages=['normalize-japanese-address'],
        version='0.1.0',
        license='MIT',
        install_requires=['janome', 'pykakasi', 'semidbm', 'six'],
        author='fanannan',
        author_email='saw@computer.org',
        url='https://github.com/fanannan/normalize-japanese-address',
        description='To normalize Japanese address.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        keywords='address geo map',  # PyPIでの検索用キーワードをスペース区切りで指定
        classifiers=[
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 3.8',
                ],
        )
