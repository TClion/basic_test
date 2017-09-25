#!/usr/bin/env python
# coding=utf8

# version:1.0
# kali linux python 2.7.13
# author:TClion
# update:2017-09-11
# pymongo 练习


import pymongo


class Mongo():
    def __init__(self, dbname, coll_name):
        self.client = pymongo.MongoClient('localhost', 27017)    #连接数据库
        # self.db = self.client.dbname
        self.db = self.client[dbname]       #连接数据库
        # self.coll = self.db.collection_name
        self.coll = self.db[coll_name]      #连接表

    #插入一条数据
    def insert(self):
        info = {'name': 'john', 'age': '20'}
        id = self.coll.insert(info)
        print id

    #删除一条数据
    def remove(self):
        data = {'name': 'john'}
        remove_info = self.coll.remove(data)
        print remove_info

    #更新数据
    def update(self):
        # self.coll.update_many({'name': 'john'}, {'$set': {'age': '22'}})    #更新多条数据
        # self.coll.update({'name': 'john'}, {'$set': {'age': '25'}},multi=True)    #更新多条数据
        self.coll.update({'name': 'john'}, {'$set': {'age': '25'}})         #更新一条数据

    #查找一条记录
    def find_one(self):
        info = self.coll.find_one()
        info2 = self.coll.find_one({'name': 'john'})
        print info, info2

    #列出所有记录
    def find(self):
        loops = self.coll.find()
        for item in loops:
            print item

    #排序
    def sort(self):
        loops = self.coll.find().sort('age', pymongo.DESCENDING)  #降序
        new_loops = self.coll.find().sort('age', pymongo.ASCENDING)  #升序
        for item in new_loops:
            print item

if __name__ == '__main__':
    M = Mongo('school', 'student')      #dbname coll_name
    M.insert()
    M.update()
    # M.find()
    M.find()
    # M.find_one()
    # M.find()
    # print M.coll.count()      #查看数据个数
    # M.coll.remove()     #删除表
    # M.sort()



