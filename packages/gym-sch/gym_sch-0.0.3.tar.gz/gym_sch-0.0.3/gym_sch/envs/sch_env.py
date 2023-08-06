#!E:\Pycharm Projects\Waytous
# -*- coding: utf-8 -*-
# @Time : 2022/9/24 14:47
# @Author : Opfer
# @Site :
# @File : sch_env.py    
# @Software: PyCharm

#!E:\Pycharm Projects\Waytous
# -*- coding: utf-8 -*-
# @Time : 2022/9/24 14:28
# @Author : Opfer
# @Site :
# @File : foo_env.py
# @Software: PyCharm


"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from https://webdocs.cs.ualberta.ca/~sutton/book/code/pole.c
"""

import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import copy
import bisect
import sys
from typing import List
# from . import sim_py_v5
# from .sim_py_v5 import get_para, env_reset

from . import sim_py_v5
from .sim_py_v5 import get_para, env_reset

T, payload = get_para("T&p")
dump_num, shovel_num, truck_num = get_para("mnt")
com_time, go_time, loading_time, unloading_time = get_para("time")
dis = get_para("dis")
fuel_speed_empty, fuel_speed_heavy = get_para("fuel_speed")
(
    empty_power,
    heavy_power,
    idle_power,
    shovel_idle_power,
    shovel_work_power,
) = get_para("energy")
shovel_target_mass, dump_target_mass = get_para("target")
empty_speed, heavy_speed = get_para("speed")

logger = logging.getLogger(__name__)


class TruckScheduleEnv(gym.Env):

    def __init__(self):
        """
        环境信息
        """
        self.shovel_num = shovel_num
        self.destinations = dump_num
        self.truck_num = truck_num

        """
        设备信息
        """

        self.truck_num = truck_num
        self.shovel_num = shovel_num
        self.dump_num = dump_num

        self.empty_speed = empty_speed
        self.heavy_speed = heavy_speed
        # 矿卡空载行驶能耗
        self.empty_power = empty_power
        # 矿卡重载行驶能耗
        self.heavy_power = heavy_power
        # 矿卡空转能耗
        self.idle_power = idle_power
        # 电铲闲置能耗
        self.shovel_idle_power = shovel_idle_power
        # 电铲装载能耗
        self.shovel_work_power = shovel_work_power
        # 有效载荷
        self.payload = np.full((1, truck_num), payload)
        # 平均每吨出产消耗燃料下限
        self.lb_feul_production = 3
        # 自适应权重值，初始为0.7
        self.adaptive_weighting = 0.7

        self.now = 0

        self._seed()

        self.viewer = None

        '''
        定义动作空间及状态空间
        '''

        # 动作空间 [0,1,2,3,4,5,...],前面是挖机后面是卸点 最后是对权重的调整
        # self.action_space = spaces.Discrete(self.shovel_num + self.dump_num)
        self.action_space = spaces.Tuple([spaces.Discrete(self.shovel_num + self.dump_num), spaces.Discrete(10)])
        # self.action_space = spaces.Discrete(2 * (self.shovel_num + self.dump_num))

        # 状态信息：请求调度车辆位置,  行驶时间, 预期等待时间, 当前自适应权重[0, 1]
        obs_high = np.r_[self.shovel_num + self.dump_num,
                         np.zeros(self.shovel_num + self.dump_num),
                         np.zeros(self.shovel_num + self.dump_num), 1].reshape(1, -1)
        obs_low = np.r_[0,
                        np.zeros(self.shovel_num + self.dump_num),
                        np.zeros(self.shovel_num + self.dump_num), 0].reshape(1, -1)

        self.observation_space = \
            spaces.Box(low=obs_low, high=obs_high, shape=(1, 2 + 2 * (self.shovel_num + self.dump_num)), dtype=int)

        self.machine_num = (self.shovel_num + self.dump_num)    # 装载及卸载设备数量

    def _reset(self, train_mode: bool):
        """
        Reset the environment.
        :return: environment state
        """

        # 初始化状态
        self.current_request_truck = 0                                   # 当前请求调度的车辆编号
        self.wait_truck_num = np.zeros(self.shovel_num + self.dump_num)  # 等待设备服务的车辆数
        self.current_request_location = 0                                # 当前请求调度的车辆位置
        self.goto_destination_time = np.zeros(self.shovel_num + self.dump_num)  # 驶往各目的地的时间
        self.waiting_time = np.zeros(self.shovel_num + self.dump_num)    # 各目的地的等待时间

        # 初始化当前时间
        self.now = 0

        # 重置仿真环境
        env_reset(train_mode)

        self._seed()
        self.viewer = None

        return self._get_current_state_representation()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action: List[int]):
        """
        Motivate the simulation go ahead until next dispatching request.
        :param action: dispatching destination
        :return: environment state, reward, simulation over signal, machine utilization, throughput, adaptive weight
        """
        reward = 0.0

        self.current_request_location, reward, self.adaptive_weighting, utilization, mass, heu_rpm = self._sim_step(action)

        if self._is_done():
            return self._get_current_state_representation(), reward, self._is_done(), {}, utilization, mass, self.adaptive_weighting, heu_rpm
        return self._get_current_state_representation(), reward, False, {}, utilization, mass, self.adaptive_weighting, heu_rpm

    def _sim_step(self, action: List[int]):
        """
        Simulation environment API.
        :param action:
        :return: request location, reward, adaptive weight, machine utilization, throughput
        """
        self.current_request_location, \
        self.goto_destination_time, \
        self.waiting_time, self.now, \
        reward, weight, utilization, \
        mass, heu_rpm = sim_py_v5.sim_step(action[0], action[1])
        return self.current_request_location, reward, weight, utilization, mass, heu_rpm

    def _is_done(self):
        """
        Return true if the simulation process is over.
        """
        if self.now * 480 >= T:
            return True
        return False

    def _get_current_state_representation(self):
        """
        Integrate environment state and return.
        """
        return np.r_[self.current_request_location, self.goto_destination_time, self.waiting_time, self.adaptive_weighting]

    def _render(self, mode='human', close=False):
        pass
