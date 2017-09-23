#!/usr/bin/env
# coding=utf8

# version:1.0
# kali linux python 2.7.13
# author:TClion
# update:2017-09-23
# redis 练习


import redis

class Redis_test():

    def __init__(self):
        self.conn = redis.Redis('localhost', 6379)

    # string type 一个键对应一个值
    def str_test(self):
        self.conn.set('name', 'john')   #赋值
        self.conn.set('age', 20)
        name = self.conn.get('name')    #取值
        age = self.conn.get('age')
        print name, age
        self.conn.mset({'id': 15, 'phone': 122345})     #设多个值
        value = self.conn.mget(['id', 'phone'])         #取多个值
        print value
        self.conn.delete('phone')    #删除一个键
        phone = self.conn.get('phone')  #返回None
        print phone
        self.conn.incr('age')   #增加值
        self.conn.incr('age', 10)
        self.conn.decr('id')    #减少值
        self.conn.decr('id', 10)
        print self.conn.get('age'),self.conn.get('id')

    # list type 字符串队列
    def list_test(self):
        table = 'zoo'
        self.conn.lpush(table, 'duck')  #左增值
        self.conn.linsert(table, 'before', 'duck', 'bear')  #在duck值之前插入bear
        self.conn.linsert(table, 'after', 'duck', 'fish')   #在duck之后插入fish
        self.conn.lset(table, 1, 'cat') #在偏移量为1处插入cat
        self.conn.ltrim(table, 1, 4)    #取范围内的值
        self.conn.rpush(table, 'bird')  #右增加值bird
        print self.conn.lindex(table, 0)    #取到偏移量为0的值
        print self.conn.lrange(table, 0, -1)    #取所有值

    # hash type
    def hash_test(self):
        table = 'student'
        self.conn.hmset(table, {'name': 'john', 'age': '19'})   #添加多个值
        self.conn.hset(table, 'id', '100')  #增加一个值
        print self.conn.hget(table, 'id')   #id键对应的值
        print self.conn.hmget(table, 'id', 'name')  #多个键对应的值
        print self.conn.hkeys(table)        #所有key
        print self.conn.hvals(table)        #所有value
        print self.conn.hlen(table)         #表长度
        print self.conn.hgetall(table)      #整个表

    # set type
    def set_test(self):
        table = 'zoo2'
        self.conn.sadd(table, 'duck', 'bear')   #添加值
        print self.conn.scard(table)    #表数量
        print self.conn.smembers(table)   #表所有值
        self.conn.srem(table, 'duck')   #删除duck

if __name__ == '__main__':
    R = Redis_test()
    R.str_test()
    # R.list_test()
    # R.hash_test()
    # R.set_test()

