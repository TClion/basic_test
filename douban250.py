#!/usr/bin/env python
# coding=utf8

import time
import redis
import gevent
import requests
import pymongo

from lxml import etree
from gevent.queue import Queue

from gevent import monkey
monkey.patch_all()


class spider():
    def __init__(self):
        self.Url = 'https://movie.douban.com/top250?start='
        self.lst_page = [self.Url+str(i) for i in xrange(0, 250, 25)]
        self.Q = Queue()
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['movie']
        self.coll = self.db['top250']



    def parse_info_url(self, url):
        page = requests.get(url).content
        data = etree.HTML(page)
        url_lst = data.xpath('//ol[@class="grid_view"]/li//div[@class="hd"]/a/@href')
        for i in url_lst:
            self.Q.put_nowait(i)
            print i

    def parse_info(self):
        while True:
            if self.Q.empty():
                time.sleep(0.05)
                print '1'
                continue
            url = self.Q.get_nowait()
            info = self.parse(url)
            if self.coll.find_one({'url':url}) == None:
                self.coll.insert(info)
                print 'insert success'

    def parse(self, url):
        page = requests.get(url).content
        data = etree.HTML(page)
        title = data.xpath('//h1/span[1]/text()')[0]
        post = {
            'url': url,
            'title': title,
        }
        return post


if __name__ == '__main__':
    top250_movie = spider()
    thread = [gevent.spawn(top250_movie.parse_info_url, i) for i in top250_movie.lst_page]
    thread.append(gevent.spawn(top250_movie.parse_info))
    gevent.joinall(thread)



