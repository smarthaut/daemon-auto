#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/29 上午11:28
# @Author  : huanghe
# @Site    : 
# @File    : get_carid.py
# @Software: PyCharm
from utils.file_manage import ExcelReader,YamlReader
import json
from utils.cookie_manage import get_pwd_cookie
from utils.xmldao import dateDao
from src.common.common import BaseHttp
from utils.xml_gen import get_xubao
from utils.log import Logger
import time

#获取报价元数据
#后续需要添加根据品牌型号查询
class CarId():
    def __init__(self,filename,province,city,iscity,date,district=''):
        self.province = province
        self.city = city
        self.iscity = iscity
        self.cookie = get_pwd_cookie('mul')
        self.district = district
        self.date =date
        self.logger = Logger('car_id').get_logger()
        get_xubao(filename=filename,province=self.province,city=self.city,iscity=self.iscity,district=self.district,date=self.date)
        self.fg = dateDao(filename)

    def get_duojia_data_info(self,casename):
        Ereader = ExcelReader(sheet='duojia', excel=YamlReader('config.yml').get_data('data'))
        data = Ereader.get_value(casename)
        url = data['url']
        params = json.loads(data['params'])
        method = data['method']
        return url, params, method

    def accesss(self,url,params,method):
        basehttp = BaseHttp(method=method, timeout=150)
        basehttp.set_url(url)
        if url == '/yiiapp/car-ins/record-price-info':
            basehttp.set_data(params)
        else:
            basehttp.set_params(params)
        return basehttp

    def get_car_id(self):
        try:
            url, params, method = self.get_duojia_data_info('test_get_car_model_no_info')
            for key in params:
                params[key] = self.fg.getValueByName(key)
            basehttp = self.accesss(url, params, method)
            basehttp.set_cookie(self.cookie)
            r = basehttp.get_post()
            if len(r.json()['data']) ==0:
                pass
            else:
                # 添加选取价格最近的车辆
                diff = []
                for i in range(len(r.json()['data'])):
                    diffvalue = abs(
                        r.json()['data'][i]['price'] / float(10000) - float(self.fg.getValueByName('price')))
                    diff.append(diffvalue)
                index = diff.index(min(diff))
                self.fg.setValueByName('price', value=str(r.json()['data'][index]['price'] / float(10000)))
                self.fg.setValueByName('seat_num', value=str(r.json()['data'][index]['seat']))
                self.fg.setValueByName('selected_car_model_detail',
                                       value=json.dumps(r.json()['data'][index], sort_keys=True, indent=4,
                                                        separators=(',', ':'),
                                                        ensure_ascii=False))
            url, params, method = self.get_duojia_data_info('test_replenish_info_merge')
            for key in params:
                params[key] = self.fg.getValueByName(key)
            basehttp = self.accesss(url, params, method)
            basehttp.set_cookie(self.cookie)
            r = basehttp.get_post()
            self.fg.setValueByName('car_id', value=str(r.json()['data']['car_id']))
            url, params, method = self.get_duojia_data_info('test_update')
            for key in params:
                params[key] = self.fg.getValueByName(key)
            basehttp = self.accesss(url, params, method)
            basehttp.set_cookie(self.cookie)
            r = basehttp.get_post()
            try:
                self.fg.setValueByName('post_time_stamp',value=time.strftime('%Y-%m-%d %H:%M:%S'))
                #self.fg.setValueByName('post_time_stamp', value=r.json()['data']['post_time_stamp'])
                self.fg.setValueByName('customer_id', value=str(r.json()['data']['customer_id']))
            except:
                assert False
            url, params, method = self.get_duojia_data_info('test_price_config')
            for key in params:
                params[key] = self.fg.getValueByName(key)
            basehttp = self.accesss(url, params, method)
            basehttp.set_cookie(self.cookie)
            r = basehttp.get_post()
            self.logger.info(r.json())
            carid = self.fg.getValueByName('car_id')
            insure_company = []
            for i in range(len(r.json()['data']['ins_companies'])):
                if r.json()['data']['ins_companies'][i]['is_open'] == 1:
                    company = r.json()['data']['ins_companies'][i]['company']
                    self.fg.setValueByName('display_name',value=r.json()['data']['ins_companies'][i]['display_name'])
                    insure_company.append(company)
            return carid, insure_company
        except:
            carid = ''
            insure_company = ''
            return carid, insure_company

def get_insurance_company(province,city):
    basehttp = BaseHttp( method='post',timeout=150)
    basehttp.set_cookie(get_pwd_cookie('mul'))
    basehttp.set_url('/yiiapp/car-ins/price-configuration')
    param = {}
    param['province'] = province
    param['city'] = city
    basehttp.set_params(param)
    r = basehttp.get_post()
    insure_company = []
    for i in range(len(r.json()['data']['ins_companies'])):
        if r.json()['data']['ins_companies'][i]['is_open'] == 1:
            company = r.json()['data']['ins_companies'][i]['company']
            insure_company.append(company)
    return insure_company


if  __name__ =='__main__':
    #carid = CarId(filename='浙江_绍兴.xml',province='浙江',city='绍兴',iscity=0,district='柯桥区',date='2018-03-01')
    #print(carid.get_car_id())
    print(get_insurance_company(province='浙江',city='嘉兴'))