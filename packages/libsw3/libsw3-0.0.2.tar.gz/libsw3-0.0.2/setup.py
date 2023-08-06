#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="libsw3",
    version="0.0.2",
    author="Chen chuan",
    author_email="kcchen@139.com",
    description="libsw3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    data_files=[
        ('/usr/local/bin',['bin/swn']),
    ],
    entry_points={
        'console_scripts':  [
            'sw=bin.sw',
        ],
    },
)
