#!/bin/python3
#
# Copyright (c) 2022 北京实耐固连接技术有限公司,Inc.All rights reserved. 
#
# File Name:        config.py
# Author:           Liu Fengchen <fengchen.liu@sng.com.cn>
# Created:          8/23/22 Tue
# Description:      配置模块相关代码。
import os
import yaml


class Config:
    """
    SNG系列软件配置文件接口，目的是统一配置文件目录和格式，仅使用简单的接口即可读取配置文件。
    配置文件位于/etc/sng/<config name>.yaml
    """

    def __init__(self, name):
        self.path = "/etc/sng/" + name + ".yaml"
        assert os.path.exists(self.path), self.path + " not found!"

        self.encode = "utf-8"
        self.mode = "r"

    def is_exist(self) -> bool:
        """
        判断传入的配置名称对应的文件是否存在。
        :return: 返回文件是否存在。
        """
        return os.path.exists(self.path)

    def read(self):
        """
        读取配置文件内容，可使用下标方式读取。
        注意：该方法只负责原模原样读取，若遇到路径数据，需要使用general模块的parse_path处理才可使用。
        :return: 返回配置文件数据。
        """
        assert Config.is_exist(self), self.get_file_name() + " 不存在！"

        with open(self.path, self.mode, encoding=self.encode) as fr:
            return yaml.load(fr, Loader=yaml.SafeLoader)

    def get_file_name(self) -> str:
        """
        获取配置文件完整路径。
        :return: 返回配置文件完整路径。
        """
        return self.path
