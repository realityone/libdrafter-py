#!/usr/bin/env python
import os

from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

install_requires = [
   'cffi>=1.9.1',
   'pycparser>=2.17'
]

setup(
    name="libdrafter-py",
    version='0.1.1',
    description="Drafter binding for python.",
    url='https://github.com/realityone/libdrafter-py',
    packages=['libdrafter'],
    install_requires=install_requires,
    zip_safe=False,
    include_package_data=True,
)
