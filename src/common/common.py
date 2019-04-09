#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/5 上午9:21
# @Author  : huanghe
# @Site    : 
# @File    : common.py
# @Software: PyCharm
import requests
from utils.path import Path
from utils.file_manage import YamlReader

class BaseHttp:

    def __init__(self,method,host=YamlReader('config.yml').get_data('env'),timeout = 60):
        self.method = method
        #设置超时时间
        self.host = host
        self.timeout = timeout
        self.headers = {}
        self.data = {}
        self.params={}


    def set_url(self,url):
        self.url =self.host+url

    def set_headers(self,header):
        self.headers = header

    def set_params(self,param):
        self.params = param

    def set_data(self,data):
        self.data = data

    def set_cookie(self,cookie):
        self.cookie = cookie

    def set_file(self,filename):
        if filename != '':
            file_path = Path().basepath+ filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    def get_post(self):
        try:
            if self.method == 'get':
                response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(self.timeout),cookies = self.cookie)
                return response
            elif self.method == 'post':
                response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data,
                                         timeout=float(self.timeout),cookies = self.cookie)
                return response
        except TimeoutError:
            return None

    def post_file(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(self.timeout))
            return response
        except TimeoutError:
            return None
    def post_json(self):
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(self.timeout))
            return response
        except TimeoutError:
            return None

if __name__ == '__main__':
    pass

