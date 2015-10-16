#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='iss',
    version='0.1',
    description="Ideally Single Source app for Salesforce data.",
    author='Bob Erb',
    author_email='bob.erb@aashe.org',
    url='https://github.com/aashe/iss',
    long_description=read("README.md"),
    packages=[
        'iss',
        'iss.migrations'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    install_requires=["Django==1.8.4",
                      "beatboxxx==21.5"]
)
