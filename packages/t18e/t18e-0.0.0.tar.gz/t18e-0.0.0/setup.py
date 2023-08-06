#!/usr/bin/env python3
# -*- encoding: utf-8
# SPDX-License-Identifier: MIT
# Copyright (c) https://github.com/scott91e1 ~ 2021 - 2021

__banner__ = r""" (

    A Paranoid Personal/Family/Friends EA Powered by Python + 4TH








)





"""  # __banner__

import setuptools

long_description = "# TBA"

__version__ = "0.0.0"

setuptools.setup(
    name="t18e",
    version=__version__,
    author="Scott McCallum <https://linkedin.com/in/scott-mccallum>",
    author_email="CTOs@Urbane.eMail",
    description="A Paranoid Personal/Family/Friends EA Powered by Python + 4TH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theprojectwith/noname",
    packages=setuptools.find_packages(),
    install_requires=[
        "simplejson"
    ],
    entry_points={"console_scripts": ["t18e=t18e.run"]},
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Forth",
        "Topic :: Education",
        "Topic :: Multimedia",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.7",
)
