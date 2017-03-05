#!/usr/bin/env  python3

from setuptools import setup

setup(
    name='challenge',
    version='1.0',
    description='Supporting library for challenges like those on stepik.org.',
    url='https://github.com/elmar-hinz/Learn.Bioinformatics.Python',
    author='Elmar Hinz',
    author_email='t3elmar@gmail.com',
    license='MIT',
    packages=['challenge', 'HelloWorld'],
    entry_points={
        'console_scripts': [
            'challenge=challenge.main:main',
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
