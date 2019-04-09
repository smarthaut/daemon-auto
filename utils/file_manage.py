#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 上午9:29
# @Author  : huanghe
# @Site    : 
# @File    : file_manage.py
# @Software: PyCharm
import yaml
import os
from utils.path import Path
from xlrd import open_workbook,xldate_as_tuple
import datetime
import xlrd
import xlwt
import json
from xlutils.copy import copy

class YamlReader:
    def __init__(self,yaml):
        #yaml:文件名
        if os.path.exists(Path().get_config_path(yaml)):
            self.yaml =Path().get_config_path(yaml)
        else:
            raise FileNotFoundError('配置文件不存在')
        self._data = None
    @property
    def data(self):
        if not self._data:
            with open(self.yaml,'rb')as f:
                self._data = list(yaml.safe_load_all(f))
                #self._data = list(yaml.safe_load_all(f))
        return self._data

    def get_data(self,element,index=0):
        return self.data[index].get(element)

    def set_data(self,value,index=0):
        data = self.data[index]
        data['num']=value
        with open(self.yaml, 'w')as f:
            yaml.dump(data, f)

#Excel文件读取
class SheetTypeError(Exception):
    pass

class ExcelReader:
    """
    读取excel文件中的内容。返回list。

    如：
    excel中内容为：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |

    如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    可用于做接口自动化
    """
    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(os.path.join(Path().basepath,'data',excel)):
            self.excel = os.path.join(Path().basepath,'data',excel)
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # 首行为title
                list_value = []
                num = 1
                for col in range(1, s.nrows):
                    str_obj = {}
                    for i in range(len(s.row_values(0))):
                        ctype = s.cell(num, i).ctype
                        cell = s.cell_value(num, i)
                        if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                            cell = int(cell)  # 浮点转成整型
                            cell = str(cell)  # 转成整型后再转成字符串，如果想要整型就去掉该行
                        elif ctype == 3:
                            year, month, day, hour, minute, second = xldate_as_tuple(cell, 0)
                            date = datetime.datetime(year, month, day)
                            cell = datetime.datetime.strftime(date, '%F')
                        elif ctype == 4:
                            cell = True if cell == 1 else False
                        str_obj[title[i]] = cell
                    list_value.append(str_obj)
                    num = num + 1
                    # 依次遍历其余行，与首行组成dicos.path.dirname(os.path.abspath(__file__))t，拼到self._data中
                self._data = list_value
            else:
                for col in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data

    def get_value(self,value):
        for data in self.data:
            if data['casename'] == value:
                return data


    def get_list_len(self):
        return len(self.data)

#向excel写数据,
date = datetime.datetime.now().strftime('%Y-%m-%d')
filename = 'result_' + date + '.xls'
def write_excel_xls(filename,sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    path = os.path.join(Path().basepath,'result',filename)
    workbook.save(path)  # 保存工作簿


def write_excel_xls_append(value):
    index = len(value)  # 获取需要写入数据的行数
    path = os.path.join(Path().basepath, 'result', filename)
    try:
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
        for i in range(0, index):
            for j in range(0, len(value[i])):
                new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
        new_workbook.save(path)  # 保存工作簿
    except:
        book_name_xls = filename
        sheet_name_xls = 'result'
        value_title = [["用户", "车牌号", "车架号", "car_id", "order_id","省份", "城市","区","机构","保险公司", "报价结果","返点", "核保结果", "时间"]]
        write_excel_xls(book_name_xls, sheet_name_xls, value_title)
        write_excel_xls_append(value)


def write_mul_insured(value):
    index = len(value)  # 获取需要写入数据的行数
    path = os.path.join(Path().basepath, 'result', filename)
    try:
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
        for i in range(0, index):
            for j in range(0, len(value[i])):
                new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
        new_workbook.save(path)  # 保存工作簿
    except:
        book_name_xls = filename
        sheet_name_xls = 'result'
        value_title = [["省份", "城市", "保险公司"]]
        write_excel_xls(book_name_xls, sheet_name_xls, value_title)
        write_excel_xls_append(value)








if __name__ == '__main__':
    #yreader = YamlReader('num.yml')
    #yreader.set_data(element='num',value=4)
    #print(yreader.get_data('num'))
    #print(yreader.get_data('mysql'))
    #print(yreader.get_data('env'))
    #values = [["豫A12345", "123214", "河南", "商丘", "成功", "失败"]]
    #write_excel_xls_append(values)
    #print(get_li_beg('广西','南宁'))
    #list= get_source()
    #print(list)
    #reader = ExcelReader(excel='neimenggu_single.xls')
    #data = reader.data
    #print(data[0])
    pass
