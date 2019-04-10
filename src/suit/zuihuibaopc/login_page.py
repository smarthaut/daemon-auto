#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/3 下午6:08
# @Author  : huanghe
# @Site    : 
# @File    : login_page.py
# @Software: PyCharm
from utils.log import Logger
from src.common.base_page import Basepage
from src.suit.zuihuibaopc.main_page import MainPage

class LoginPage(Basepage):
	def rec_user_input(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.logger.debug(u'找到"请输入手机号"输入input.')
		return self.find_element(selector='x=>//*[@id="main"]/div/div[2]/div/div[2]/div[1]/input')

	def rec_passwd_input(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.logger.debug(u'找到"请输入密码密码"输入input.')
		return self.find_element(selector='x=>//*[@id="main"]/div/div[2]/div/div[2]/div[2]/input')

	def rec_login_btn(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.logger.debug(u'找到"登录"按钮.')
		return self.find_element(selector='x=>//*[@id="main"]/div/div[2]/div/div[2]/div[4]/button')

	def click_login_btn(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.rec_login_btn().click()
		self.logger.debug(u'点击"登录 "按钮.')
		return MainPage(self.driver)