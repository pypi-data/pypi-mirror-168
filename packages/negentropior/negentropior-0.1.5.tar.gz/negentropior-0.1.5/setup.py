#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='negentropior',
      version='0.1.5',
      description='ILabor algorithm group tools 算法组常用工具方法',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Yi OuYang, ZhiWen Wang',
      author_email='yiouyang143@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[],
      classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
          ],
)


