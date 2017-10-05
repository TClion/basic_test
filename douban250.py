#!/usr/bin/env python
# coding=utf8

# version:1.0
# kali linux python 2.7.13
# author:TClion
# update:2017-10-06
# 豆瓣top250电影信息抓取，redis去重，数据存入mongodb中


import time
import redis
import gevent
import random
import pymongo
import requests

from lxml import etree
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()

class spider():
    def __init__(self):
        self.Url = 'https://movie.douban.com/top250?start='
        self.lst_page = [self.Url+str(i) for i in xrange(0, 250, 25)]
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.R = redis.Redis(host='localhost', port=6379)
        self.db = self.conn['douban']
        self.data_coll = self.db['top250']
        self.ip_coll = self.conn['ipdb']['ip_good']
        self.insert_success_num = 0     #抓取成功数量
        self.ip_lst = self.get_ip_lst_m()
        self.ip = random.choice(self.ip_lst)
        self.pool = Pool(100)

    #从ip库中读取ip
    def get_ip_lst_m(self):
        ip_lst = []
        for item in self.ip_coll.find():
            ip_str = item['ip']
            ip = ip_str.split(':')[0]
            port = ip_str.split(':')[1]
            new_ip_str = 'http://' + ip + ':' + port
            ip_dict = {
                'http': new_ip_str,
                'https': new_ip_str,
            }
            ip_lst.append(ip_dict)
        return ip_lst

    #抓取列表页url
    def parse_info_url(self, url):
        while True:
            try:
                page = requests.get(url, proxies=self.ip, timeout=5)
                break
            except:
                try:
                    self.ip_lst.remove(self.ip)
                    self.ip = random.choice(self.ip_lst)
                except:
                    print 'ip list empty'
                    self.ip_lst = self.get_ip_lst_m()
        content = page.text
        data = etree.HTML(content)
        print '%s parse successful' % url
        url_lst = data.xpath('//ol[@class="grid_view"]/li//div[@class="hd"]/a/@href')
        self.pool.map(self.parse, url_lst)

    #抓取详情页信息
    def parse(self, url):
        if url in self.R.smembers('doubanbook') and self.data_coll.find_one({'url': url}):
            return
        while True:
            try:
                page = requests.get(url, proxies=self.ip, timeout=5)
                break
            except:
                try:
                    self.ip_lst.remove(self.ip)
                    self.ip = random.choice(self.ip_lst)
                except:
                    print 'ip list empty'
                    self.ip_lst = self.get_ip_lst_m()
        content = page.text
        data = etree.HTML(content)
        try:
            title = data.xpath('//h1/span[1]/text()')[0]
        except:
            return
        post = {
            'url': url,
            'title': title,
        }
        self.data_coll.insert(post)
        self.insert_success_num += 1
        self.R.sadd('doubanbook', url)
        print '%s parse successful' % url


if __name__ == '__main__':
    T1 = time.time()
    douban = spider()
    thread = [gevent.spawn(douban.parse_info_url, i) for i in douban.lst_page]
    gevent.joinall(thread)
    T2 = time.time()
    print douban.insert_success_num
    print T2-T1



