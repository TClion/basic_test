#!/usr/bin/env python
# coding=utf8

# version:1.0
# kali linux python 2.7.13
# author:TClion
# update:2017-11-24
# collections.deque 基础练习

from collections import deque

d = deque('abcdef')

print 'deque:', d
print 'length:', len(d)

d.remove('c')

print 'remove c:', d

d.extend('ghijk')

print 'extend ghijk', d

d.extendleft('01234')

print 'extend 01234', d

d.append('l')

print 'append l:', d

d.appendleft(100)

print 'appendleft 100', d

number_pop = d.pop()

print 'pop:', d, number_pop

number_popleft = d.popleft()

print 'popleft:', d, number_popleft


