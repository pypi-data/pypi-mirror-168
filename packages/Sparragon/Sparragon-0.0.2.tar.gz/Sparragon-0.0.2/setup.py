#!/usr/bin/env python

from setuptools import setup
from sparragon import VERSION

setup(
  name             = 'Sparragon',
  version          = VERSION,
  description      = 'Python library to interact with Galaxy Life ',
  author           = 'Folfy Blue',
  url              = 'http://github.com/twoolie/NBT',
  license          = open("LICENSE").read(),
  long_description = open("README.md").read(),
  packages         = ['sparragon'],
)