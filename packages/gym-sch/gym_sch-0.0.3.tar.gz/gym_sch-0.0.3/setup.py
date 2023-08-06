#!E:\Pycharm Projects\Waytous
# -*- coding: utf-8 -*-
# @Time : 2022/9/24 14:46
# @Author : Opfer
# @Site :
# @File : setup.py
# @Software: PyCharm

from setuptools import setup
import setuptools
from pathlib import Path

setup(name='gym_sch',
      version='0.0.3',
      install_requires=['gym'],
      description='An OpenAI Gym Env for Pandas',
      long_description=Path('README.md').read_text(),
      long_description_content_type='text/markdown',
      packages=setuptools.find_packages(include='gym_sch*')
)
