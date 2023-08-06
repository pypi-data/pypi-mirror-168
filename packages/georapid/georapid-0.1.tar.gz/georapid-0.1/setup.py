# Copyright (C) 2022 Jan Tschada (gisfromscratch@live.de)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

"""
Install with python setup.py sdist bdist_wheel
"""

with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='georapid',
    version='0.1',
    author='Jan Tschada',
    author_email='gisfromscratch@live.de',
    description='Query broadcasted news worldwide and visualize them using spatial aggregations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Geospatial-AI-DE/georapid-py',
    packages=['georapid'],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
     ]
 )
