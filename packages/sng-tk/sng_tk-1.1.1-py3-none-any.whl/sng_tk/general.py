#!/bin/python3
#
# Copyright (c) 2022 北京实耐固连接技术有限公司,Inc.All rights reserved. 
#
# File Name:        general.py
# Author:           Liu Fengchen <fengchen.liu@sng.com.cn>
# Created:          8/23/22 Tue
# Description:      通用接口，提供简单的函数调用。
import os


def print_header():
    """
    以带颜色文本的形式输出SNG Logo，并在右侧显示公司名称、官网以及联系方式。
    """
    print("\n", flush=True)
    print("\033[31m       ■■■■■■■■■■■\033[34m ■■■■■■■■■■■■■■■■\033[0m    ", flush=True)
    print("\033[31m    ■■■■■■■■■■■■■■\033[34m ■■■■■■■■■■■■■■■■\033[0m    ", flush=True)
    print("\033[31m   ■■■■■■■■■■■■■■■\033[34m ■■■■■■■■■■■■■■■■\033[0m    ", flush=True)
    print("\033[31m  ■■■■■■■■■■■■■■■■\033[34m ■■■■■■■■■■■■■■■■\033[0m    ", flush=True)
    print("\033[31m   ■■■■■■■■■■■■■■■\033[34m ■■■■■■■■■■■■■■■■\033[0m   ┌────────────────SNG───────────────┐", flush=True)
    print("\033[31m    ■■■■■■■■■■■■■■\033[34m ■■■■■■■■■■■■■■■■\033[0m   │ Website :https://www.sng.com.cn/ │", flush=True)
    print("\033[31m       ■■■■■■■■■■■\033[34m ■■■■■■■■■■■■■■■■\033[0m   │ E-mail  :sng@sng.com.cn          │", flush=True)
    print("\033[34m  ■■■■■■■■■■■■■■■■\033[31m ■■■■■■■■■■■■    \033[0m   │ TEL     :010-61567220            │", flush=True)
    print("\033[34m  ■■■■■■■■■■■■■■■■\033[31m ■■■■■■■■■■■■■■  \033[0m   │ Fax     :010-61567336            │", flush=True)
    print("\033[34m  ■■■■■■■■■■■■■■■■\033[31m ■■■■■■■■■■■■■■■ \033[0m   └──────────────────────────────────┘", flush=True)
    print("\033[34m  ■■■■■■■■■■■■■■■■\033[31m ■■■■■■■■■■■■■■■■\033[0m    ", flush=True)
    print("\033[34m  ■■■■■■■■■■■■■■■■\033[31m ■■■■■■■■■■■■■■■ \033[0m    ", flush=True)
    print("\033[34m  ■■■■■■■■■■■■■■■■\033[31m ■■■■■■■■■■■■■■  \033[0m    ", flush=True)
    print("\033[34m  ■■■■■■■■■■■■■■■■\033[31m ■■■■■■■■■■■■    \033[0m    ", flush=True)
    print("\n", flush=True)


def parse_path(path):
    """
    可处理路径中含有的一些特殊字符，将其转换为绝对路径。
    如：
    1.路径开头为“~”的，将其替换为用户主目录： ~/path => /home/user/path
    """
    if path[0] == "~":
        path = path[1:]
        path = os.getenv("HOME") + path
    path = os.path.abspath(path)
    return path
