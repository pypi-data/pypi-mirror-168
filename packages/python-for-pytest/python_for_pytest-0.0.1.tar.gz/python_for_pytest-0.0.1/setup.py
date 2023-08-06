#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# DevVersion: Python3.6.8
# Date: 2022-09-19 19:35
# Author: SunXiuWen
# PyCharm|setup.py

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

# with open('requirements.txt', "r", encoding="utf-8") as f:
#     requirements = f.readlines()
requirements = ['attrs', 'colorama==0.4.5', 'contextlib2', 'execnet==1.9.0', 'iniconfig==1.1.1', 'json-flatten==0.2', 'mock==4.0.3', 'packaging==21.3', 'path==16.4.0', 'path.py==12.5.0', 'pluggy==1.0.0', 'py==1.11.0', 'pyparsing==3.0.9', 'pytest==7.1.3', 'pytest-shutil==1.7.0', 'six==1.16.0', 'termcolor==2.0.1', 'tomli==2.0.1', 'xlrd==2.0.1', 'xlwt==1.3.0']

setuptools.setup(
    name="python_for_pytest",  # 库名
    version="0.0.1",  # 版本号
    author="SunXiuWen",  # 作者
    author_email="xiuwensun@163.com",  # 作者邮箱
    description="It is simple and fast to use unit testing",  # 包的简单说明
    long_description=long_description,  # 包的详细说明
    long_description_content_type="text/markdown",  # README.md中描述的语法（一般为markdown）
    url="http://github.com",  # 项目地址
    install_requires=requirements,  # 模块需要的依赖包
    packages=setuptools.find_packages(),  # 包列表
    classifiers=[  # 包标签，便于搜索
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
)
