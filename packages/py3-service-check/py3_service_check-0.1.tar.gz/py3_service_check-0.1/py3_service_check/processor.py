#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/22 8:33 上午
# @Author  : Meng Wang
# @Site    :
# @File    : processor.py
# @Software: PyCharm
import time

from influxdb import InfluxDBClient
import datetime
import socket
from loguru import logger
import vthread

"""
核心处理器
"""

INFLUX_MEASUREMENT_PREFIX = "monitor_"
# 获取主机名
hostname = socket.gethostname()
# 获取IP
host_ip = socket.gethostbyname(hostname)


class Exposer(object):
    """
        应用名称  event-merger
    """
    app_name = None
    """
        influxdb 主机 192.168.100.207
    """
    influx_host = None
    """
        influxdb 数据库
    """
    influx_db = 'intelab'
    """
        influxdb 端口
    """
    influx_port = 8086
    """
        influxdb 用户名
    """
    influx_user = "admin"
    """
        influxdb 密码
    """
    influx_password = 'admin'
    """
        存储策略
    """
    influx_rp = None

    """
        检测任务多久跑一次 也就是定时器的timer 默认60（s）
    """
    timer_duration = 60

    def __init__(self, app_name, influx_host, influx_db, influx_port, influx_user, influx_password, influx_rp,
                 timer_duration):
        self.app_name = app_name
        self.influx_host = influx_host
        self.influx_db = influx_db
        self.influx_user = influx_user
        self.influx_password = influx_password
        self.influx_port = influx_port
        self.influx_rp = influx_rp
        self.timer_duration = timer_duration

    def expose_data_to_influxdb(self):
        conn_db = InfluxDBClient(self.influx_host, str(self.influx_port), self.influx_user, self.influx_password,
                                 self.influx_db)
        current_time = datetime.datetime.utcnow().isoformat("T")
        timer_data = [
            {
                "measurement": INFLUX_MEASUREMENT_PREFIX + self.app_name,
                "time": current_time,
                "tags": {
                    "ip": host_ip
                },
                "fields": {"status": 1.0}
            }
        ]

        conn_db.write_points(points=timer_data, retention_policy=self.influx_rp)  # 写入数据，同时创建表
        logger.debug("{} monitor job added succeed!", self.app_name)
        conn_db.close()

    @vthread.pool(1)
    def init_work_main_thread(self):
        while True:
            self.expose_data_to_influxdb()
            time.sleep(self.timer_duration)

    """
        任务执行
    """

    def start(self):
        self.init_work_main_thread()
