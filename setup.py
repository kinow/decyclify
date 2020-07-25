#!/usr/bin/env python

# Copyright 2020 Bruno P. Kinoshita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

from decyclify import __version__ as version

install_requires = [
    'networkx==2.4.*'
]

tests_require = [
    'pytest==5.4.*',
    'coverage==5.2.*',
    'pytest-cov==2.10.*'
]

extras_require = {
    'all': []
}
extras_require['all'] = (
    tests_require
    + list({
        req
        for reqs in extras_require.values()
        for req in reqs
    })
)

setup(
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    version=version,
    packages=find_packages(include=["decyclify.*"]),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    project_urls={
        "Documentation": "https://github.com/kinow/decyclify",
        "Source": "https://github.com/kinow/decyclify",
        "Tracker": "https://github.com/kinow/decyclify/issues"
    }
)
