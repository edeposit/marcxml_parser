#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from docs import getVersion


changelog = open('CHANGES.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    changelog
])


setup(
    name='marcxml_parser',
    version=getVersion(changelog),
    description="MARC XML / OAI parser, with few highlevel getters.",
    long_description=long_description,
    url='https://github.com/edeposit/marcxml_parser',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,

    zip_safe=False,
    install_requires=[
        'setuptools',
        "pyDHTMLParser>=2.0.7",
        "remove_hairs",
        "enum34",
    ],
    extras_require={
        "test": [
            "pytest"
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    },
)
