#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 下午1:42
# @Author  : huanghe
# @Site    : 
# @File    : conftest.py
# @Software: PyCharm
'''import pytest
from utils.file_reader import ExcelReader
from utils.config import Config

#pytest_plugins = 'allure.pytest_plugin'
@pytest.fixture
def record_common_car_info():
    url = (ExcelReader(sheet=3, excel=Config().get('data')).data)[0]['url']
    params = (ExcelReader(sheet=3, excel=Config().get('data')).data)[0]['params']
    method = (ExcelReader(sheet=3, excel=Config().get('data')).data)[0]['method']
    return url,params,method
    '''
import pytest
import allure
from utils.file_manage import ExcelReader
from utils.file_manage import YamlReader
import json

Ereader = ExcelReader(sheet=3, excel=YamlReader('config.yml').get_data('data'))

@pytest.fixture
def make_customer_record():
    def _make_customer_record(name):
        return {
            "name":name,
            "order":[]
        }
    return _make_customer_record

@pytest.fixture
def get_data_info():
    def _get_data_info(casename):
        data = Ereader.get_value(casename)
        url = data['url']
        params = json.loads(data['params'])
        method =data['method']
        return url,params,method
    return _get_data_info

@pytest.fixture
def get_duojia_data_info():
    def _get_data_info(casename):
        Ereader = ExcelReader(sheet='duojia', excel=YamlReader('config.yml').get_data('data'))
        data = Ereader.get_value(casename)
        url = data['url']
        params = json.loads(data['params'])
        method =data['method']
        return url,params,method
    return _get_data_info

@pytest.fixture
def get_single_data_info():
    def _get_data_info(casename):
        Ereader = ExcelReader(sheet='single', excel=YamlReader('config.yml').get_data('data'))
        data = Ereader.get_value(casename)
        url = data['url']
        params = json.loads(data['params'])
        method =data['method']
        return url,params,method
    return _get_data_info

@pytest.fixture
def env(request):
    env_config = YamlReader('config.yml').get_data('env')
    allure.environment(host=env_config)
    return env_config
