#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 下午2:09
# @Author  : huanghe
# @Site    : 
# @File    : test_login.py
# @Software: PyCharm
import unittest
from utils.browser import Browser
from src.suit.zuihuibaopc.login_page import LoginPage
from utils.file_reader import Config
import time

class ZuiTest(unittest.TestCase):

	def setUp(self):
		self.driver = Browser().get_browserdriver()
		self.login_page = LoginPage(self.driver)
		self.config = Config().get('ZPC')
		self.login_page.url = self.config.get('url')
		self.login_page.visit()
		self.login_page.wait(5)
		self.login_page.set_value(element=self.login_page.rec_user_input(), text=self.config.get('user'))
		self.login_page.set_value(element=self.login_page.rec_passwd_input(), text=self.config.get('pwd'))
		self.main_page = self.login_page.click_login_btn()

	def tearDown(self):
		pass
		#self.driver.quit()        self.logger = Logger(loggername=self.classname).get_logger()


	def test_login(self):
		time.sleep(5)
		self.main_page.rec_order_manage()


