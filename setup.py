#!/usr/bin/env python

import os

from setuptools import setup, find_packages

import versioneer


description = long_description = (
    'BigQuery shell built with ibis and prompt_toolkit'
)


with open(
    os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'rt'
) as f:
    install_requires = list(map(str.strip, f))

setup(
    name='bqsh',
    url='https://github.com/cpcloud/bqsh',
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'bqsh = bqsh.bqsh:main',
        ],
    },
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
    license='Apache License, Version 2.0',
    maintainer='Phillip Cloud',
    maintainer_email='phillip.cloud@twosigma.com'
)
