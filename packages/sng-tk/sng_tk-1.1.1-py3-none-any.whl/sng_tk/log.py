#!/bin/python3
#
# Copyright (c) 2022 北京实耐固连接技术有限公司,Inc.All rights reserved. 
#
# File Name:        log.py
# Author:           Liu Fengchen <fengchen.liu@sng.com.cn>
# Created:          8/23/22 Tue
# Description:      日志模块。
import logging
import os
import threading

import colorlog
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
from sng_tk import Config as SConfig
from sng_tk import general as SGeneral


class Log:
    """
    先实例化该类的对象，构造函数参数为日志配置文件名，该文件名对应目录为/etc/sng/<config name>.yaml
    该文件必须存在。
    :param conf: 日志配置文件，默认为log
    """
    __log_colors_config = {
        # 终端输出日志颜色配置
        'DEBUG': 'white',
        'INFO': 'cyan',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    __default_formats = {
        # 终端输出格式
        'color_format': '%(log_color)s'
                        '%(asctime)s-{filename}[line:{line}]-%(levelname)s-[日志信息]: %(message)s',
        # 日志输出格式
        'log_format': '%(asctime)s-{filename}[line:{line}]-%(levelname)s-[日志信息]: %(message)s'
    }

    def __init__(self, conf):
        if type(conf) == str:
            self.conf = SConfig(conf).read()["log"]
        else:
            if 'log' in conf.keys():
                self.conf = conf["log"]
            else:
                self.conf = conf
        # 为存放日志的路径
        self.log_path = SGeneral.parse_path(self.conf["directory"])
        # 日志等级
        self.log_level = self.conf["level"]
        # 日志开关
        self.log_close = self.conf["close"]

        self.__lock = threading.Lock()
        self.__init_logger_file()
        self.__now_time = datetime.now().strftime('%Y-%m-%d')  # 当前日期格式化
        self.__all_log_path = os.path.join(self.log_path, self.__now_time + "-all" + ".log")  # 收集所有日志信息文件
        self.__error_log_path = os.path.join(self.log_path, self.__now_time + "-error" + ".log")  # 收集错误日志信息文件
        self.__logger = logging.getLogger()  # 创建日志记录器
        self.__logger.setLevel(logging.DEBUG)  # 设置默认日志记录器记录级别

    def __init_logger_file(self):
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)  # 若不存在logs文件夹，则自动创建

    @staticmethod
    def __init_logger_handler(log_path, log_size):
        """
        创建日志记录器handler，用于收集日志
        :param log_path: 日志文件路径
        :param log_size: 日志大小Mb
        :return: 日志记录器
        """
        # 写入文件，如果文件超过1M大小时，切割日志文件，仅保留3个文件
        logger_handler = RotatingFileHandler(
            filename=log_path,
            maxBytes=log_size * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        return logger_handler

    @staticmethod
    def __init_console_handle():
        """
        创建终端日志记录器handler，用于输出到控制台。
        :return:
        """
        console_handle = colorlog.StreamHandler()
        return console_handle

    def __set_log_handler(self, logger_handler, level=logging.DEBUG):
        """
        设置handler级别并添加到logger收集器
        :param logger_handler: 日志记录器
        :param level: 日志记录器级别
        """
        logger_handler.setLevel(level=level)
        self.__logger.addHandler(logger_handler)

    def __set_color_handle(self, console_handle):
        """
        设置handler级别并添加到终端logger收集器
        :param console_handle: 终端日志记录器
        """
        console_handle.setLevel(logging.DEBUG)
        self.__logger.addHandler(console_handle)

    def __set_color_formatter(self, console_handle, color_config):
        """
        设置输出格式-控制台
        :param console_handle: 终端日志记录器
        :param color_config: 控制台打印颜色配置信息
        :return:
        """
        line_number = sys._getframe(3).f_lineno
        filename = sys._getframe(3).f_code.co_filename
        ignorePrefix = SGeneral.parse_path(self.conf["ignore_code_path_mask"])
        if filename[:len(ignorePrefix)] == ignorePrefix:
            filename = filename[len(ignorePrefix):]

        formatter = colorlog.ColoredFormatter(Log.__default_formats["color_format"].format(filename=filename, line=line_number), log_colors=color_config)
        console_handle.setFormatter(formatter)

    def __set_log_formatter(self, file_handler):
        """
        设置日志输出格式-日志文件
        :param file_handler: 日志记录器
        """
        line_number = sys._getframe(3).f_lineno
        filename = sys._getframe(3).f_code.co_filename
        ignorePrefix = SGeneral.parse_path(self.conf["ignore_code_path_mask"])
        if filename[:len(ignorePrefix)] == ignorePrefix:
            filename = filename[len(ignorePrefix):]

        formatter = logging.Formatter(Log.__default_formats["log_format"].format(filename=filename, line=line_number), datefmt='%a, %d %b %Y %H:%M:%S')
        file_handler.setFormatter(formatter)

    @staticmethod
    def __close_handler(file_handler):
        """
        关闭handler
        :param file_handler: 日志记录器
        """
        file_handler.close()

    def __console(self, level, message):
        """
        构造日志收集器
        :param level:
        :param message:
        :return:
        """
        # 若关闭日志则什么也不做。
        if self.log_close:
            return

        self.__lock.acquire()

        message = ' '.join([str(x) for x in message])

        all_logger_handler = self.__init_logger_handler(self.__all_log_path, self.conf["max_size"])
        error_logger_handler = self.__init_logger_handler(self.__error_log_path, self.conf["max_size"])
        console_handle = self.__init_console_handle()

        self.__set_log_formatter(all_logger_handler)  # 设置日志格式
        self.__set_log_formatter(error_logger_handler)
        self.__set_color_formatter(console_handle, Log.__log_colors_config)

        self.__set_log_handler(all_logger_handler)  # 设置handler级别并添加到logger收集器
        self.__set_log_handler(error_logger_handler, level=logging.ERROR)
        self.__set_color_handle(console_handle)

        if level == 'debug' and self.log_level <= 0:
            self.__logger.debug(message)
        elif level == 'info' and self.log_level <= 1:
            self.__logger.info(message)
        elif level == 'warning' and self.log_level <= 2:
            self.__logger.warning(message)
        elif level == 'error' and self.log_level <= 3:
            self.__logger.error(message)
        elif level == 'critical' and self.log_level <= 4:
            self.__logger.critical(message)

        self.__logger.removeHandler(all_logger_handler)  # 避免日志输出重复问题
        self.__logger.removeHandler(error_logger_handler)
        self.__logger.removeHandler(console_handle)

        self.__close_handler(all_logger_handler)  # 关闭handler
        self.__close_handler(error_logger_handler)

        self.__lock.release()

    def debug(self, *message):
        self.__console('debug', message)

    def info(self, *message):
        self.__console('info', message)

    def warning(self, *message):
        self.__console('warning', message)

    def error(self, *message):
        self.__console('error', message)

    def critical(self, *message):
        self.__console('critical', message)

    def set_option(self, key, value):
        self.conf[key] = value
