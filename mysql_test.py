#!/usr/bin/python
# -*- coding: UTF-8 -*-

# version:1.0
# kali linux python 2.7.13
# author:TClion
# update:2017-11-10
# MySQLdb的基础操作，包括增删改查等

import MySQLdb


class mysql():
    def __init__(self, user='root', password='password', dbname='TESTDB'):
        self.db = MySQLdb.connect('localhost', user, password, dbname)
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        self.table_name = "EMPLOYEE"

    def create_table(self):
        sql = """CREATE TABLE EMPLOYEE 
        (FIRST_NAME VARCHAR(20),LAST_NAME VARCHAR(20),AGE INT,SEX VARCHAR(20),INCOME FLOAT)"""
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print e
            self.db.rollback()

    def delete_table(self):
        sql = "DROP TABLE %s" % self.table_name
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print e
            self.db.rollback()

    def insert_data(self):
        sql = """INSERT INTO %s(FIRST_NAME,
                 LAST_NAME, AGE, SEX, INCOME)
                 VALUES ('Mac', 'Mohan', 20, 'M', 2000)""" % self.table_name
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print e
            self.db.rollback()

    def delete_data(self):
        sql = "DELETE FROM %s WHERE AGE > '%d'" % (self.table_name, 20)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print e
            self.db.rollback()

    def update_data(self):
        sql = "UPDATE %s SET AGE = AGE + 1 WHERE SEX = '%c'" % (self.table_name, 'M')
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print e
            self.db.rollback()

    def find_data(self):
        sql = """SELECT * FROM %s WHERE AGE = %d""" % (self.table_name, 21)
        try:
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                print row
        except Exception as e:
            print e
            self.db.rollback()

    def do(self, sql=None):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print e
            self.db.rollback()

if __name__ == '__main__':
    mydb = mysql()
    mydb.insert_data()
    mydb.update_data()
    mydb.find_data()
    # mydb.delete_table()
    mydb.cursor.close()
    mydb.db.close()
