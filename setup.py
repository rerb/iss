#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='iss',
    version='2.4.2',
    description="Ideally Single Source app for Salesforce data.",
    author='Scott Johnson',
    author_email='scott@aashe.org',
    url='https://github.com/aashe/iss',
    long_description=read("README.md"),
    packages=[
        'iss',
    ],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    install_requires=["Django>=1.4,<1.9",
                      "beatbox==32.1",
                     "membersuite-api-client>=0.1.15",
                     ]
)
