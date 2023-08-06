# denodo/setup.py
#
# Copyright (C) 2005-2018 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
#
# This software is part of the DenodoConnect component collection and
# is based on the PostgreSQL dialect of SQLAlchemy.
# Copyright (c) 2022, denodo technologies (http://www.denodo.com)
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from codecs import open
from os import path
from setuptools import setup


THIS_DIR = path.dirname(path.realpath(__file__))

with open(path.join(THIS_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='denodo-sqlalchemy',
    version='20220919',
    description='Denodo Dialect for SQLAlchemy',
    long_description=long_description,
    author='Denodo Research Labs',
    author_email='research.labs@denodo.com',
    license='MIT license',
    url='https://www.denodo.com',
    keywords="Denodo db database",
    download_url='https://www.denodo.com',
    use_2to3=False,

    namespace_packages=[
        'denodo'
    ],
    packages=[
        'denodo.sqlalchemy',
    ],
    package_dir={
        'denodo.sqlalchemy': '.',
    },
    package_data={
        'denodo.sqlalchemy': ['LICENSE'],
    },
    entry_points={
        'sqlalchemy.dialects': [
            'denodo=denodo.sqlalchemy:dialect',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Topic :: Database',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    install_requires=[
        'sqlalchemy<2.0.0,>=1.4.0',
        'psycopg2-binary>=2.7',
    ],
    extras_require={
        'development': [
            'pytest',
        ]
    },
)