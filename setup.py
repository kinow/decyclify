#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

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
