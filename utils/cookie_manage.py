#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 上午10:32
# @Author  : huanghe
# @Site    : 
# @File    : cookie_manage.py
# @Software: PyCharm
#获取用户cookie并存储
import requests
from utils.path import Path
from utils.file_manage import YamlReader

offline_mobile = YamlReader('config.yml').get_data('User').get('mul_user')
offline_pwd = YamlReader('config.yml').get_data('User').get('mul_pwd')
single_mobile = YamlReader('config.yml').get_data('User').get('single_user')
single_pwd = YamlReader('config.yml').get_data('User').get('single_pwd')
url_pwd_url = 'https://www.zhbbroker.com/yiiapp/user-pwd/user-pwd-login?mobile='+str(offline_mobile)+'&pwd='+offline_pwd
url_pwd_url_s = 'https://www.zhbbroker.com/yiiapp/user-pwd/user-pwd-login?mobile='+str(single_mobile)+'&pwd='+single_pwd

#type 1 多家 2 单家
def set_pwd_cookie(type):

    if str(type) == '2':
        url = url_pwd_url_s
    else:
        url = url_pwd_url
    s = requests.session()
    response = s.post(url)
    cookies = response.cookies.get_dict()
    with open(Path().get_cookie_path(),'w')as f:
        f.write(str(cookies))
    f.close()

def get_pwd_cookie(type):
    if type == 'mul':
        set_pwd_cookie(1)
    else:
        set_pwd_cookie(2)
    with open(Path().get_cookie_path(),'r')as f:
        text = f.read()
    f.close()
    return eval(text)

if __name__ =='__main__':
    get_pwd_cookie('single')
