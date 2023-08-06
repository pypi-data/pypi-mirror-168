#!/usr/bin/env python

from setuptools import setup
from sparragon import VERSION

setup(
  name             = 'Sparragon',
  version          = VERSION,
  description      = 'Python library to interact with Galaxy Life ',
  author           = 'Folfy Blue',
  url              = 'http://github.com/twoolie/NBT',
  license          = "GPL",
  long_description = open("README.md").read(),
  long_description_content_type="text/markdown",
  packages         = ['sparragon'],
)