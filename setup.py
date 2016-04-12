#!/usr/bin/env python
# vim: set fileencoding=utf8 shiftwidth=4 tabstop=4 textwidth=80 foldmethod=marker :
# Copyright (c) 2010, Kou Man Tong. All rights reserved.
# Copyright (c) 2015, Ayun Park. All rights reserved.
# For licensing, see LICENSE file included in the package.

from setuptools import setup

setup(
    name="bson",
    version="0.4.3",
    packages=["bson"],
    install_requires=["pytz>=2010b", "six>=1.9.0"],
    author="Ayun Park",
    author_email="iamparkayun@gmail.com",
    description="BSON codec for Python",
    long_description="""Independent BSON codec for Python that doesn't depend on MongoDB.""",
    platforms="Any",
    license="BSD",
    keywords="BSON codec",
    url="http://github.com/py-bson/bson",
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
