#!/bin/python3
#
# Copyright (c) 2022 北京实耐固连接技术有限公司,Inc.All rights reserved.
#
# File Name:        __init__.py
# Author:           Liu Fengchen <fengchen.liu@sng.com.cn>
# Created:          8/14/22 Sun
# Description:      存放常用的接口的引入。
import time as __time

from .config import Config
from .log import Log
from . import general as General
from .mqtt_client import MQTTClient

# 在任何导入该包的程序中输出SNG的logo和信息，因为python对于模块的导入是
# 单例的，因此这里不需要额外进行任何处理。
General.print_header()
__time.sleep(0.1)
