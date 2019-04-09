#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/29 上午11:05
# @Author  : huanghe
# @Site    : 
# @File    : xml_gen.py
# @Software: PyCharm
from xml.dom import minidom
from utils.file_manage import YamlReader,ExcelReader
from utils.path import Path
from utils.dbhelper import MysqlHelper
import os
from utils.data_gen import get_li_beg
from utils.log import Logger
log = Logger('xml_gen').get_logger()

def get_xubao(filename,province,city,iscity,district,date,company='',):
    province = province
    city = city
    company = company
    district = district
    config = YamlReader('config.yml')
    date = date
    host = config.get_data('mysql').get('host')
    port = config.get_data('mysql').get('port')
    user = config.get_data('mysql').get('user')
    passwd = config.get_data('mysql').get('passwd')
    db = config.get_data('mysql').get('db')
    helper = MysqlHelper(host=host,port=port,db= db,user=user,passwd=passwd)
    #result = helper.get_xubao(province,city,data)
    if iscity == 1:
        liben = get_li_beg(province=province,city=city)+'%'
        result = helper.get_xubao(province=province,city=liben,company=company,date=date)
    else:
        result = helper.get_xubao(province=province,company=company,date=date)
    if len(result) == 0:
        dictdata = {'engine_no':'','seat_num':''}
    else:
        dictdata = result[0]
    print(dictdata)
    dictinsure = config.get_data('insured')
    dictdata = dict(dictdata, **dictinsure)
    dictdata['version'] = config.get_data('app').get('version')
    dictdata['insurance_company'] = company
    dictdata['city'] = city
    if dictdata['engine_no'] == '':
        dictdata['engine_no'] = '321352'
    if dictdata['seat_num'] == 0:
        dictdata['seat_num'] = 4
    dictdata['district'] = district
    dictdata['addressee_name'] =  '张汉'
    dictdata['addressee_mobile'] =  '17621100888'
    dictdata['addressee_province'] =  province
    dictdata['addressee_city'] = city
    dictdata['addressee_area'] =  district
    dictdata['addressee_detail'] =  '南京路新华小区102室'
    dictdata['insured_mobile'] = '17621100888'
    dictdata['applicant_mobile'] = '17621100888'
    dictdata['owner_mobile'] = '17621100888'
    dictdata['insured_province'] = province
    dictdata['insured_city'] = city
    dictdata['insured_district'] = district
    dictdata['insured_detail'] = '南京路新华小区102室'
    impl = minidom.getDOMImplementation()
    doc = impl.createDocument(None, None, None)
    rootElement = doc.createElement('dates')
    for key, value in dictdata.items():
        # 创建子元素
        childElement = doc.createElement('date')
        # 为子元素添加id属性
        childElement.setAttribute('name', str(key))
        childElement.setAttribute('value', str(value))
        # 将子元素追加到根元素中
        rootElement.appendChild(childElement)
        # 将拼接好的根元素追加到dom对象
        doc.appendChild(rootElement)
        # 打开test.xml文件 准备写入
    filename = os.path.join(Path().get_data_path(),filename)
    f = open(filename, 'w', encoding='UTF-8')
    # 清空数据
    f.seek(0)
    f.truncate()
    # 写入文件
    doc.writexml(f, addindent=' ', newl='\n', encoding='UTF-8')
    # 关闭
    f.close()

def get_xubao_xml(filename,province,city,iscity,district,date,company='',):
    config = YamlReader('config.yml')
    reader = ExcelReader('suzhou_single.xls')
    n= int(YamlReader('num.yml').get_data('num'))
    dictdata = reader.data[n]
    #记录+1
    n = n+1
    YamlReader('num.yml').set_data(n)
    dictinsure = config.get_data('insured')
    dictdata = dict(dictdata, **dictinsure)
    dictdata['version'] = config.get_data('app').get('version')
    dictdata['insurance_company'] = company
    dictdata['city'] = city
    if dictdata['engine_no'] == '':
        dictdata['engine_no'] = '321352'
    if dictdata['seat_num'] == 0:
        dictdata['seat_num'] = 4
    dictdata['district'] = district
    dictdata['addressee_name'] =  '张汉'
    dictdata['addressee_mobile'] =  '17621100888'
    dictdata['addressee_province'] =  province
    dictdata['addressee_city'] = city
    dictdata['addressee_area'] =  district
    dictdata['addressee_detail'] =  '南京路新华小区102室'
    dictdata['insured_mobile'] = '17621100888'
    dictdata['applicant_mobile'] = '17621100888'
    dictdata['owner_mobile'] = '17621100888'
    dictdata['insured_province'] = province
    dictdata['insured_city'] = city
    dictdata['insured_district'] = district
    dictdata['insured_detail'] = '南京路新华小区102室'
    impl = minidom.getDOMImplementation()
    doc = impl.createDocument(None, None, None)
    rootElement = doc.createElement('dates')
    for key, value in dictdata.items():
        # 创建子元素
        childElement = doc.createElement('date')
        # 为子元素添加id属性
        childElement.setAttribute('name', str(key))
        childElement.setAttribute('value', str(value))
        # 将子元素追加到根元素中
        rootElement.appendChild(childElement)
        # 将拼接好的根元素追加到dom对象
        doc.appendChild(rootElement)
        # 打开test.xml文件 准备写入
    filename = os.path.join(Path().get_data_path(),filename)
    f = open(filename, 'w', encoding='UTF-8')
    # 清空数据
    f.seek(0)
    f.truncate()
    # 写入文件
    doc.writexml(f, addindent=' ', newl='\n', encoding='UTF-8')
    # 关闭
    f.close()

if __name__ == '__main__':
    get_xubao_xml(filename='suzhou_single.xml', province='安徽', city='宿州', date='2018-04-25', district='灵璧支公司', iscity=0)
