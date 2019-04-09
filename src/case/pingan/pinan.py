#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/27 上午11:34
# @Author  : huanghe
# @Site    : 
# @File    : pinan.py
# @Software: PyCharm
from src.common.common import BaseHttp



http = BaseHttp(method='post',host='http://www.pingan.com')
http.set_url('/property_insurance/pa18AutoInquiry/queryRepairStoreList.do')
http.set_params()