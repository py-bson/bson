#!/usr/bin/env python
# vim: set fileencoding=utf8 shiftwidth=4 tabstop=4 textwidth=80 foldmethod=marker :
# Copyright (c) 2010, Kou Man Tong. All rights reserved.
# Copyright (c) 2015, Ayun Park. All rights reserved.
# For licensing, see LICENSE file included in the package.
import sys
import importlib.util
from setuptools import setup
from setuptools.command.install import install


class NewInstall(install):

    @staticmethod
    def check_pymongo():
        return importlib.util.find_spec('pymongo')

    def run(self):
        install.run(self)
        if self.check_pymongo():
            sys.stdout.write('\033[31mCaution! \033[33mbson(pymongo) is already installed.\033[0m\n')


setup(
    name="bson",
    version="0.5.10",
    packages=["bson"],
    install_requires=["python-dateutil>=2.4.0", "six>=1.9.0"],
    author="Ayun Park",
    author_email="iamparkayun@gmail.com",
    description="BSON codec for Python",
    long_description="""Independent BSON codec for Python that doesn't depend on MongoDB.""",
    platforms="Any",
    license="BSD",
    keywords="BSON codec",
    url="http://github.com/py-bson/bson",
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    cmdclass={'install': NewInstall}
)
