#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 下午6:05
# @Author  : huanghe
# @Site    : 
# @File    : learn.py
# @Software: PyCharm
# coding=utf-8
import threading
from utils.path import Path
import os


class Find(threading.Thread):
    def __init__(self, kaifanglist, istart, iend, searchstr, savefile):
        threading.Thread.__init__(self)
        self.kaifanglist = kaifanglist  # 开放数据的内存地址
        self.istart = istart  # 开始的索引
        self.iend = iend  # 结束的索引
        self.seachstr = searchstr  # 需要搜索的数据
        self.savefile = savefile  # 保存

    def run(self):
        self.findlist = []
        for i in range(self.istart, self.iend):
            line = self.kaifanglist[i].decode("gbk", "ignore")  # 读取一行
            if line.find(self.seachstr) != -1:
                print(self.getName(), line, end="----")  # 搜索数据
                self.findlist.append(line)  # 找到加入列表
        global mutex
        with mutex:  # 写入
            for line in self.findlist:
                self.savefile.write(line.encode("utf-8"))  # 写入


mutex = threading.Lock()  # 创建一个锁
savefile = open(os.path.join(Path().get_data_path(),'result_2019-03-14.xls'),'wb')
#savefile = open("C:\\Users\\pc\\Desktop\\zhaolin.txt", "wb")

path = "C:\\Users\\pc\\Desktop\\kaifangX.txt"
file = open(path, "rb")
kaifanglist = file.readlines()  # 全部读入内存
lines = len(kaifanglist)  # 所有的行数
searchstr = input("输入要查询的数据")
N = 10  # 开启10个线程
threadlist = []
# 97 9    0-1000000  1000000-2000000  2000000-3000000
for i in range(0, N - 1):  # 0,1,2,3,4,5,6,7,8  数据切割
    mythd = Find(kaifanglist, i * (lines // (N - 1)), (i + 1) * (lines // (N - 1)), searchstr, savefile)
    mythd.start()
    threadlist.append(mythd)

# 97 =  97//10*10=90
mylastthd = Find(kaifanglist, lines // (N - 1) * (N - 1), lines, searchstr, savefile)
mylastthd.start()
threadlist.append(mylastthd)

for thd in threadlist:
    thd.join()

print("finish")
savefile.close()  # 关闭
