#!/usr/bin/env python
import os

from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

with open(os.path.join(SOURCE_DIR, 'requirements.txt'), 'r') as f:
    requirements = f.read().splitlines()

setup(
    name="libdrafter-py",
    version='0.1',
    description="Drafter binding for python.",
    url='https://github.com/realityone/libdrafter-py',
    packages=['libdrafter'],
    install_requires=requirements,
    zip_safe=False,
)
