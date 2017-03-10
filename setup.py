#!/usr/bin/env  python3

from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Read version from central version file
with open(path.join(here, 'version.txt'), encoding='utf-8') as f:
    version = f.read().strip()

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='challenges',
    version=version,
    description='Library to assist programming, testing and execution '
                + 'of solutions for coding challenges like those on '
                  'stepik.org',
    long_description=long_description,
    keywords='education stepik coursera bioinformatics challenges',
    url='https://github.com/elmar-hinz/Python.Challenges',
    author='Elmar Hinz',
    author_email='t3elmar@gmail.com',
    license='MIT',
    packages=['challenges', 'HelloWorld'],
    package_data={
        'HelloWorld': ['sample.txt', 'result.txt'],
        'challenges': ['version.txt'],
        },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'challenge=challenges:main',
            'stepik=challenges:main',
        ],
    },
    scripts=['bin/challenge'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Education :: Computer Aided Instruction (CAI)',
    ],
)
