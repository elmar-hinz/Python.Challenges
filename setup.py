#!/usr/bin/env  python3

from os.path import dirname, realpath

from setuptools import setup

version_file = realpath(dirname(__file__)) + '/version.txt'

with open(version_file) as f:
    version = f.read().strip()

setup(
    name='challenges',
    version=version,
    description='Library to assist programming, testing and execution '
                + 'of solutions for coding challenges like those on '
                  'stepik.org',
    url='https://github.com/elmar-hinz/Python.Challenges',
    author='Elmar Hinz',
    author_email='t3elmar@gmail.com',
    license='MIT',
    packages=['challenges', 'HelloWorld'],
    entry_points={
        'console_scripts': [
            'challenge=challenges.main:main',
            'stepic=challenges.main:main',
        ],
    },
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
