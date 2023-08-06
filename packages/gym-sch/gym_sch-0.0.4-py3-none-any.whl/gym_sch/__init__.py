#!E:\Pycharm Projects\Waytous
# -*- coding: utf-8 -*-
# @Time : 2022/9/24 14:46
# @Author : Opfer
# @Site :
# @File : __init__.py.py    
# @Software: PyCharm

from gym.envs.registration import register

register(
		id='sch-v0',
		entry_point='gym_sch.envs:TruckScheduleEnv',
)