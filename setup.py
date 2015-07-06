# coding=utf-8
import os
import re

from setuptools import find_packages
from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name = "python-streamlike",
    version = "0.0.3",
    description = "Streamlike API wrapper",
    long_description = long_description,
    author = "Martin-Zack Mekkaoui",
    author_email = "martin@brightfor.me",
    license = "MIT License",
    url = "https://github.com/brightforme/python-streamlike/",
    keywords = [ 'Streamlike API wrapper','CDN', 'API' ],
    classifiers = [],
    packages = find_packages(),
    include_package_data = True,
    install_requires=['requests>=2.0.0'],
    zip_safe = False
)