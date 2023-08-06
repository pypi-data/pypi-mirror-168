#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 4:43 下午
# @Author  : Meng Wang
# @Site    : 
# @File    : test_handler.py
# @Software: PyCharm
from abc import ABCMeta, abstractmethod

"""
测试处理器  主要运行当前主要的测试流程链
"""

"""
处理器基类
"""


class Handler(metaclass=ABCMeta):
    """
        @:parameter nginx_ip
        :parameter nginx_ip
    """

    @abstractmethod
    def process(self, nginx_ip):
        pass


"""
Database
"""


class DatabaseHandler(Handler):
    def process(self, nginx_ip):
        pass
