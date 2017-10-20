#!/usr/bin/env python
# coding=utf8

# version:2.0
# kali linux python 2.7.13
# author:TClion
# update:2017-09-07
# 抓取智联招聘招聘信息，结果存放在mongodb中

import urllib
import gevent
import pymongo
import requests
from lxml import etree
from gevent.queue import Queue


header = {

    'Host': 'sou.zhaopin.com',
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Connection': "keep-alive",

}   # 必须加的header


class spider():

    def __init__(self, pagenumber=1):

        self.One_level_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?"      #源链接
        self.pagenumber = pagenumber

        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn.zhilian
        self.info_url_db = self.db.infourl
        self.info_db = self.db.info

        place = raw_input("请输入要查询的地区:")
        position = raw_input("请输入你要找的职位:")
        name = urllib.quote(place)              # 将地区变为url可识别的编码
        zw = urllib.quote(position)             # 将职位变为url可识别的编码
        self.One_level_url += 'jl=%s&kw=%s&p=' % (name, zw)  # 更新url
        self.parse_url_lst = [self.One_level_url + str(n) for n in xrange(1, pagenumber+1)]

        self.parse_url_successful = 0
        self.parse_info_successful = 0


    def parse_info_url(self,second_level_url):
        reponse = requests.get(second_level_url, headers=header)
        html = reponse.text
        data = etree.HTML(html)
        urls = data.xpath('//td[@class="zwmc"]/div/a/@href')
        for url in urls:
            if self.info_url_db.find_one({'url':url}) == None:
                try:
                    self.parse_info(url)
                    self.parse_url_successful += 1
                except Exception as e:
                    print 'url %s parse error' % url
                    print e
                    continue
                try:
                    self.info_url_db.insert({'url': url})
                except:
                    print 'url %s insert error' % url
            else:
                continue


    def parse_info(self, url):
        if 'jobs.zhaopin.com' not in url:
            return
        html = requests.get(url).text
        data = etree.HTML(html)
        company = data.xpath('//div[@class="inner-left fl"]/h2/a/text()')[0]
        money = data.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()')[0]
        update_time = data.xpath('//span[@id="span4freshdate"]/text()')[0]
        work_xingzhi = data.xpath('//ul[@class="terminal-ul clearfix"]/li[4]/strong/text()')[0]
        leibie = data.xpath('//ul[@class="terminal-ul clearfix"]/li[4]/strong/text()')[0]
        jingyan = data.xpath('//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()')[0]
        xueli= data.xpath('//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()')[0]
        renshu = data.xpath('//ul[@class="terminal-ul clearfix"]/li[7]/strong/text()')[0]
        info = data.xpath('//div[@class="tab-inner-cont"]/p')
        work_address_info = data.xpath('//div[@class="terminalpage-main clearfix"]//div[@class="tab-inner-cont"]/h2/text()')[0].strip()
        Info = ''.join([i.xpath('string(.)') for i in info]).replace('\n','').replace('\r','').strip()
        post = {
            'url': url,
            'company': company,
            'money': money,
            'update_time': update_time,
            'work_xingzhi': work_xingzhi,
            'jingyan': jingyan,
            'xueli': xueli,
            'renshu': renshu,
            'leibie': leibie,
            'info': Info,
            'work_address_info': work_address_info,
        }
        # for k, v in post.iteritems():
        #     print k, v
        try:
            self.info_db.insert(post)
            self.parse_info_successful += 1
        except:
            print 'info url %s insert error' % url


if __name__ == '__main__':
    zhilian = spider()
    for i in zhilian.parse_url_lst:
        zhilian.parse_info_url(i)
    print zhilian.parse_url_successful
    print zhilian.parse_info_successful

    # url = 'http://jobs.zhaopin.com/CZ408806830J00001457813.htm'
    # zhilian.parse_info(url)
