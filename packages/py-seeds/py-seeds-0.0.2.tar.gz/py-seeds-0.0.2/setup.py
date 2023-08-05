# -*- coding: utf-8 -*-
# @Time    : 2022/8/20 8:03 下午
# @Author  : ZiUNO
# @Email   : ziunocao@126.com
# @File    : setup.py
# @Software: PyCharm

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-seeds",  # Replace with your own username
    version="0.0.2",
    author="ZiUNO",
    author_email="ziuno@qq.com",
    description="Seed function for random, torch, torch.cuda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZiUNO/py-seeds",
    packages=setuptools.find_packages(),
    license='MIT',
    python_requires='>=3.6',
    install_requires=['numpy', 'torch']
)