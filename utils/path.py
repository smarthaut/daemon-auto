#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 上午9:30
# @Author  : huanghe
# @Site    : 
# @File    : path.py
# @Software: PyCharm
import os

class Path:
#获取文件的绝对路径

    def __init__(self):
        self.basepath = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

    #获取文件的绝对路径
    #dirname :父目录  filename:文件名
    def get_real_path(self,dirname,filename):
        return os.path.join(self.basepath,dirname,filename)

    #获取配置文件config.yml的绝对路径
    def get_config_path(self,filename):
        return os.path.join(self.basepath,'config',filename)

    #获取cookie.txt的绝对路径
    def get_cookie_path(self):
        return os.path.join(self.basepath,'data','cookie.txt')
    #获取data目录的绝对路径
    def get_data_path(self):
        return os.path.join(self.basepath,'data')

    #获取车牌号首位path
    def get_lce_path(self):
        return os.path.join(self.basepath,'data','CarPrefix.json')

    #获取log
    def get_log_path(self):
        return os.path.join(self.basepath,'log')

    #获取driver




if __name__ == '__main__':
    path = Path()
    print(Path().basepath)
    print(path.get_real_path(dirname='data',filename='appcasedate.xlsx'))