#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 下午1:36
# @Author  : huanghe
# @Site    : 
# @File    : login_page.py
# @Software: PyCharm
from utils.log import Logger
from src.common.base_page import Basepage
from src.suit.zuihuibaomanage.main_page import MainPage

class LoginPage(Basepage):

	def rec_user_input(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.logger.debug(u'找到"用户名"输入input.')
		return self.find_element(selector='id=>loginmodel-username')

	def rec_passwd_input(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.logger.debug(u'找到"密码"输入input.')
		return self.find_element(selector='id=>loginmodel-password')

	def rec_capcha_input(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.logger.debug(u'找到"验证码"输入input')
		return self.find_element(selector='id=>loginmodel-verifycode')

	def dow_capcha(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.logger.debug(u'下载验证码')
		captcha_png = self.find_element(selector='id=>captchaimg').screenshot_as_png
		with open("captcha.png", "wb+")as f:
			f.write(captcha_png)
			f.close()

	def rec_login_btn(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.logger.debug(u'找到"登录"按钮.')
		return self.find_element(selector='name=>login-button')

	def click_login_btn(self):
		self.logger = Logger(loggername=self.__class__.__name__).get_logger()
		self.rec_login_btn().click()
		self.logger.debug(u'点击"登录 "按钮.')

	def click_capche(self):
		self.find_element(selector='id=>captchaimg').click()

	def rec_p(self):
		return self.find_element(selector='xpath=>//*[@id="user-login"]/div/div/div[4]/div/div[2]/p')


	def get_main_page(self):
		return MainPage(self.driver)