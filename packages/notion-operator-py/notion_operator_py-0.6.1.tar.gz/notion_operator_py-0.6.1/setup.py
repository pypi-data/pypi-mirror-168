# -*- coding: utf-8 -*-
# @Filename : setup
# @Date : 2022-07-27-08-59
# @Project: nt-integration-sdk
import os

from setuptools import setup, find_packages


def get_version():
    return os.environ.get("ReleaseVersion", "v0.0.0")


def get_readme():
    with open("README.md", "r") as file:
        return file.read()


setup(
    name='notion_operator_py',
    version=get_version(),
    license='MIT',
    author="Stone Shi",
    author_email='github@stone-bo.com',
    description="Python Client for Notion Integration Only",
    long_description=get_readme(),
    long_description_type="text/markdown",
    packages=find_packages(),
    url='https://github.com/stone-home/notion_operator_py',
    python_requires=">=3.7, <4",
    install_requires=[
          'notion-client >= 1.0.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]

)
