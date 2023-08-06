#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='intelab_python_tool',
      version='0.0.1',
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


