#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from big_thing_py import __version__
import sys

from setuptools import setup, find_packages

sys.path.insert(0, "big_thing_py")

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="big-thing-py",
    #version=__version__,
    version="0.4.1.1",
    description="SoPIoT Thing SDK",
    author="caplab",
    author_email="caplab94@gmail.com",
    long_description=long_description,
    url="https://iris.snu.ac.kr",
    license="MIT",
    install_requires=[
        'termcolor',
        'getmac',
        'paho-mqtt',
        'requests',
        'zeroconf',
        'tqdm',
        'func_timeout',
        'pytest',
        'pylint',
        'autopep8',
        'dataclasses'],
    packages=find_packages("big_thing_py"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "big_thing_py"},
    python_requires='>=3.6',
)
