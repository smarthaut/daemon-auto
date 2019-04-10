#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/3 下午6:09
# @Author  : huanghe
# @Site    : 
# @File    : main_page.py
# @Software: PyCharm
from utils.log import Logger
from src.common.base_page import Basepage
from src.suit.zuihuibaopc.persion_order import PersonOrder
from src.suit.zuihuibaopc.order_manage import OrderManage
from src.suit.zuihuibaopc.verb_pwd import VerbPwd

class MainPage(Basepage):

	def rec_persion_order(self):
		self.logger.debug(u'找到"个人出单"按钮')
		return self.find_element(selector='x=>/html/body/div[1]/section/aside/ul/li[1]/i')

	def rec_order_manage(self):
		self.logger.debug(u'找到"订单管理"按钮')
		return self.find_element(selector='x=>/html/body/div[1]/section/aside/ul/li[2]/i')

	def rec_verb_pwd(self):
		self.logger.debug(u'找到"重置密码"按钮')
		return  self.find_element(selector='x=>/html/body/div[1]/section/aside/ul/li[3]/i')

	def click_persion_order(self):
		self.rec_persion_order().click()
		self.logger.debug(u'点击"个人出单"按钮')
		return PersonOrder(self.driver)

	def click_order_manag(self):
		self.rec_order_manage().click()
		self.logger.debug(u'点击"订单管理"按钮')
		return OrderManage(self.driver)

	def click_verb_pwd(self):
		self.rec_order_manage().click()
		self.logger.debug(u'点击"重置密码"按钮')
		return VerbPwd(self.driver)
