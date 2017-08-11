#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='iss',
    version='2.5.6',
    description="Ideally Single Source app for MemberSuite data.",
    author='AASHE',
    author_email='it@aashe.org',
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
    install_requires=[
        "beatbox==32.1",
        "membersuite_api_client==0.4.1",
        "pycountry",
    ]
)
