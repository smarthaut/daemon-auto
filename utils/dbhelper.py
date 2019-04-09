#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 下午2:12
# @Author  : huanghe
# @Site    : 
# @File    : dbhelper.py
# @Software: PyCharm
import pymysql
import random

class MysqlHelper():
    def __init__(self,host,port,db,user,passwd,charset='utf8'):
        self.host=host
        self.port=port
        self.db=db
        self.user=user
        self.passwd=passwd
        self.charset=charset
        self.cursorclass = pymysql.cursors.DictCursor

    def connect(self):
        self.conn=pymysql.connect(host=self.host,port=self.port,db=self.db,user=self.user,passwd=self.passwd,charset=self.charset,cursorclass = pymysql.cursors.DictCursor)
        self.cursor=self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self,sql,params=()):
        result=None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    def get_all(self,sql,params=()):
        list=()
        try:
            self.connect()
            self.cursor.execute(sql,params)
            list=self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list

    def insert(self,sql,params=()):
        self.__edit(sql,params)

    def update(self, sql, params=()):
        self.__edit(sql, params)

    def delete(self, sql, params=()):
        self.__edit(sql, params)

    def create(self,sql,parames=()):
        self.__edit(sql, parames)

    def __edit(self,sql,params):
        count=0
        try:
            self.connect()
            count=self.cursor.execute(sql,params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count

    def get_xubao(self,province,date,city='',company=''):
        helper = MysqlHelper(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd, charset='utf8')
        #省份
        if len(city)==0 and len(company)==0:
            sql = '''SELECT
                    c.province,
            	    c.city,
            	    c.insurance_company,
                	b.frame_no,
                	b.license_no,
                	b.car_model_no,
                	b.is_new_car,
                	b.engine_no,
                	b.seat_num,
                	b.reg_date,
                	b.owner_name,
                	b.owner_id_no,
                	b.owner_mobile,
                	b.insured_name,
                	b.insured_id_no,
                	b.insured_mobile,
                	b.applicant_name,
                	b.applicant_id_no,
                	b.applicant_mobile,
                	b.is_special_car,
                	b.is_loaned,
                	b.beneficiary,
                	b.price,
                	b.selected_car_model_detail
                FROM
                    user_order c 
                	LEFT JOIN user_order_detail b ON b.order_id = c.order_id 
                WHERE
                    c.province = %s 
                AND b.is_loaned <1  
                AND c.status =5
                AND b.license_no <> '' 
                AND c.underwrite_time > %s 
                AND b.seat_num <9
                AND b.is_special_car <>1
                AND LENGTH(b.owner_name)<10
                LIMIT %s,1;'''
            n = random.randint(0, 100)
            params = (province,date,n)
            result = helper.get_all(sql, params)
            #省份，城市
        elif len(city)!=0 and len(company)==0:
            sql = '''
            SELECT
	c.province,
	c.city,
	c.insurance_company,
	b.frame_no,
	b.license_no,
	b.car_model_no,
	b.is_new_car,
	b.engine_no,
	b.seat_num,
	b.reg_date,
	b.owner_name,
	b.owner_id_no,
	b.owner_mobile,
	b.insured_name,
	b.insured_id_no,
	b.insured_mobile,
	b.applicant_name,
	b.applicant_id_no,
	b.applicant_mobile,
	b.is_special_car,
	b.is_loaned,
	b.beneficiary,
	b.price,
	b.selected_car_model_detail 
FROM
	user_order c
	LEFT JOIN user_order_detail b ON b.order_id = c.order_id 
WHERE
	c.province =% s 
	AND c.license_no like % s
	AND b.is_loaned < 1 
	AND c.STATUS =5
	AND b.seat_num < 9 AND c.underwrite_time > % s 
	AND b.is_special_car <> 1 
	AND LENGTH( b.owner_name ) < 10 
	LIMIT % s,
	1;'''
            n = random.randint(0,100)
            params = (province,city,date,n)
            result = helper.get_all(sql, params)
            #省份，城市，公司
        elif len(city)!=0 and len(company)!=0:
            sql = '''
                        SELECT
            	c.province,
            	c.city,
            	c.insurance_company,
            	b.frame_no,
            	b.license_no,
            	b.car_model_no,
            	b.is_new_car,
            	b.engine_no,
            	b.seat_num,
            	b.reg_date,
            	b.owner_name,
            	b.owner_id_no,
            	b.owner_mobile,
            	b.insured_name,
            	b.insured_id_no,
            	b.insured_mobile,
            	b.applicant_name,
            	b.applicant_id_no,
            	b.applicant_mobile,
            	b.is_special_car,
            	b.is_loaned,
            	b.beneficiary,
            	b.price,
            	b.selected_car_model_detail 
            FROM
            	user_order c
            	LEFT JOIN user_order_detail b ON b.order_id = c.order_id 
            WHERE
            	c.province =% s 
            	AND c.city =% s 
            	AND b.is_loaned < 1 
            	AND c.STATUS =5 
            	AND c.insurance_company = %s
            	AND b.license_no <> '' 
            	AND b.seat_num < 9 AND c.underwrite_time > % s 
            	AND b.is_special_car <> 1 
            	AND LENGTH( b.owner_name ) < 10 
            	LIMIT % s,
            	1;'''
            n = random.randint(0, 100)
            params = (province, city,company,date,n)
            result = helper.get_all(sql, params)
        else:
            #省份，城市，公司，日期
            sql = '''
                        SELECT
            	c.province,
            	c.city,
            	c.insurance_company,
            	b.frame_no,
            	b.license_no,
            	b.car_model_no,
            	b.is_new_car,
            	b.engine_no,
            	b.seat_num,
            	b.reg_date,
            	b.owner_name,
            	b.owner_id_no,
            	b.owner_mobile,
            	b.insured_name,
            	b.insured_id_no,
            	b.insured_mobile,
            	b.applicant_name,
            	b.applicant_id_no,
            	b.applicant_mobile,
            	b.is_special_car,
            	b.is_loaned,
            	b.beneficiary,
            	b.price,
            	b.selected_car_model_detail 
            FROM
            	user_order c
            	LEFT JOIN user_order_detail b ON b.order_id = c.order_id 
            WHERE
            	c.province =% s 
            	AND c.city =% s 
            	AND b.is_loaned < 1 
            	AND c.STATUS =5 
            	AND b.license_no <> '' 
            	AND b.seat_num < 9 
            	AND b.is_special_car <> 1 
            	AND LENGTH( b.owner_name ) < 10 
            	LIMIT % s,1;'''
            n=random.randint(0,100)
            params = (province, city, company, date, n)
            result = helper.get_all(sql, params)
        return result



