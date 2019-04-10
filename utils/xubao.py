#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/29 下午1:35
# @Author  : huanghe
# @Site    : 
# @File    : xubao.py
# @Software: PyCharm
from utils.data_gen import get_district,get_xml_v2
from utils.get_carid import CarId,get_insurance_company
from utils.log import Logger
from utils.data_gen import get_province
from utils.file_manage import write_mul_insured
logger = Logger('参数').get_logger()

def get_alldata(date,source):
    xml_list = get_xml_v2(source)
    alldata = []
    for xml in xml_list:
        j = str(xml.split('.')[0])
        k = j.split('_')
        province = k[0]
        city = k[1]
        filename = xml
        district = get_district(province,city)
        if province == '江苏':
            iscity = 1
        else:
            iscity = 0
        insure_company = CarId(filename=filename, province=province,city=city,iscity=iscity,district=district,date=date).get_car_id()[1]
        for company in insure_company:
            data = (province, city, company, filename)
            alldata.append(data)
    return alldata
#获取多家报价的可报价的保险公司
def get_mul_insured():
    mdata = get_province()
    alldata = []
    for i in range(len(mdata)):
        province = mdata[i]['province']
        city = mdata[i]['city']
        insure_company = get_insurance_company(province,city)
        if len(insure_company) != 0:
            for company in insure_company:
                write_mul_insured([[province, city, company]])
    return alldata


if __name__ == '__main__':
    source = [{'province': '四川', 'city': '', 'district': ''}]
    alldata = get_alldata(source=source, date='2016-01-01')
    print(alldata)