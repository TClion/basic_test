#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import requests

from gevent.pool import Pool


class King(object):
    def __init__(self):
        self.Url = 'http://ip.chinaz.com/getip.aspx'
        self.R = redis.Redis(host='localhost', port=6379)
        self.redis_name = 'ip_all'

    def make_ip(self):
        for i in range(255):
            for j in range(255):
                for k in range(255):
                    for l in range(255):
                        ip = str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l)
                        self.R.sadd(self.redis_name, ip)

    def test_ip(self, ip):
        Ip = 'http://' + ip + ':' + '80'
        ip_dict = {
            'http': Ip,
            'https': Ip,
        }
        try:
            text = requests.get(Url, proxies=ip_dict, timeout=5).text
        except:
            return
        if ip in text:
            print ip

if __name__ == '__main__':
    king = King()
    p = Pool(500)
    p.map(king.test_ip, king.R.smembers(king.redis_name))
