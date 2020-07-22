#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = []

setup(
    name='decyclify',
    description='Graph decyclify algorithm implementation as in Sandnes & Sinnen paper (2004) in Python',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/kinow/decyclify',
    license='Apache License 2.0',
    license_file='LICENSE',
    platforms='any',
    python_requires='>=3.7',
    version='0.1',
    packages=find_packages(include=["decyclify.*"]),
    install_requires=install_requires,
    project_urls={
        "Documentation": "https://github.com/kinow/decyclify",
        "Source": "https://github.com/kinow/decyclify",
        "Tracker": "https://github.com/kinow/decyclify/issues"
    }
)
