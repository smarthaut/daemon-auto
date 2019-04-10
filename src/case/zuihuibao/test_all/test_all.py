#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/4 上午10:27
# @Author  : huanghe
# @Site    : 
# @File    : test_nantong_cpic.py
# @Software: PyCharm
#暂无法处理重复投保的问题
#数据来源于数据库
import pytest
import allure
from src.common.common import BaseHttp
from utils.cookie_manage import get_pwd_cookie
from utils.xmldao import dateDao
from utils.file_manage import write_excel_xls_append
from utils.xubao import get_alldata

#provinces = get_province_by_date()
#provinces = [{'province': '安徽', 'city': '', 'district': ''},{'province': '广东', 'city': '', 'district': ''}]
#result,source = test_get_alldata(source=[])
source = [{'province': '四川', 'city': '', 'district': ''}]
all_data = get_alldata(source=source, date='2016-01-01')
# 功能函数
@allure.step("url params,method分别为：{0},{1},{2}")
def accesss(url, params,method):
    basehttp = BaseHttp(method=method,timeout=150)
    basehttp.set_url(url)
    if url == '/yiiapp/car-ins/record-price-info':
        basehttp.set_data(params)
    else:
        basehttp.set_params(params)
    return basehttp





#报价
#网分销合并后需要报价前重新获取报价的省市机构
@pytest.mark.parametrize("province,city,insurance_company,filename",all_data)
def test_record_price(get_duojia_data_info,province,city,insurance_company,filename):
    fg = dateDao(filename)
    cookie = get_pwd_cookie('mul')
    user_id = cookie['user_id']
    fg.setValueByName('insurance_company',insurance_company.upper())
    url, params, method = get_duojia_data_info('test_update')
    for key in params:
        params[key] = fg.getValueByName(key)
    basehttp = accesss(url, params, method)
    basehttp.set_cookie(cookie)
    basehttp.get_post()
    url, params, method = get_duojia_data_info('test_price_config')
    for key in params:
        params[key] = fg.getValueByName(key)
    basehttp = accesss(url, params, method)
    basehttp.set_cookie(cookie)
    r = basehttp.get_post()
    for i in range(len(r.json()['data']['ins_companies'])):
        if r.json()['data']['ins_companies'][i]['company'] == insurance_company:
            fg.setValueByName('display_name',r.json()['data']['ins_companies'][i]['display_name'])
    url, params, method = get_duojia_data_info('test_record_price_info_merg')
    for key in params:
        params[key] = fg.getValueByName(key)
    basehttp = accesss(url, params, method)
    basehttp.set_cookie(cookie)
    r = basehttp.get_post()
    allure.attach('报价结果为：', "{0}".format(r.json()))
    pricr_result = r.json()['return_message']
    try:
        refund = r.json()['data']['user_refund']
        fg.setValueByName('order_id', value=r.json()['data']['order_id'])
        url, params, method = get_duojia_data_info('test_place_order')
        for key in params:
            params[key] = fg.getValueByName(key)
        basehttp = accesss(url, params, method)
        basehttp.set_cookie(cookie)
        r = basehttp.get_post()
        record_result = "订单号："+r.json()['data']['order_id']+r.json()['return_message']
        values = [[user_id,fg.getValueByName('license_no'),fg.getValueByName('frame_no')
                      ,fg.getValueByName('car_id'),fg.getValueByName('order_id'),fg.getValueByName('province'),
                   fg.getValueByName('city'),fg.getValueByName('district'),fg.getValueByName('display_name'),fg.getValueByName('insurance_company'),pricr_result,refund,record_result,
                   fg.getValueByName('post_time_stamp')]]
        write_excel_xls_append(values)
        allure.attach('核保结果为：', "{0}".format(r.json()))
        allure.attach('订单ID为：', "{0}".format(r.json()['data']['order_id']))
    except:
        message = r.json()['return_message']
        values = [[user_id, fg.getValueByName('license_no'), fg.getValueByName('frame_no')
                      , fg.getValueByName('car_id'),fg.getValueByName('order_id'), fg.getValueByName('province'),
                   fg.getValueByName('city'),fg.getValueByName('district'),fg.getValueByName('display_name'),fg.getValueByName('insurance_company'),pricr_result, "","",
                   fg.getValueByName('post_time_stamp')]]
        write_excel_xls_append(values)
        if str(message).find(u'重') != -1:
            allure.attach('报价失败，重复投保，返回结果为：', "{0}".format(r.json()['return_message']))
            allure.attach('报价失败，返回结果为：', "{0}".format(r.json()['return_message']))
            assert True
        else:
            allure.attach('报价失败，返回结果为：', "{0}".format(r.json()['return_message']))
            assert False
