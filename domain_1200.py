#!/usr/bin/env python
# coding=utf8

# version:1.0
# kali linux python 2.7.13
# author:TClion
# update:2017-11-30
# 抓取站长之家网站排行的域名，存入txt中

import requests

from lxml import etree


header = {
    "Host": "top.chinaz.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

class spider():
    def __init__(self):
        self.Url = "http://top.chinaz.com/all/index_%d.html"
        self.url_lst = [self.Url % i for i in xrange(2, 41)]
        self.url_lst.append("http://top.chinaz.com/all/")
        self.count = 0

    def Parse(self):
        with open('domain_1200.txt', 'w') as f:
            for u in self.url_lst:
                text = requests.get(u,headers=header).text
                page = etree.HTML(text)
                domain = page.xpath('//h3[@class="rightTxtHead"]/span[@class="col-gray"]/text()')
                for d in domain:
                    d = d.replace('www.', '')
                    f.write(d + '\n')
                    self.count += 1
                    print d
                    print self.count


if __name__ == '__main__':
    domain = spider()
    domain.Parse()

