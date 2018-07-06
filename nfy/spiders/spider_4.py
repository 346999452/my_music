#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_4
    @date: 2018/06/19
    
"""
from scrapy import Spider


'''
    用于测试请求的浏览器，cookie，源ip等
'''
class exam_spider(Spider):
    name = 'exam'

    ''' 设置爬取范围 '''
    allowed_domains = ['nfy.fun']

    start_urls = [
        'http://nfy.fun/ac/lala',
    ]

    def parse(self, response):
        print(response.body.decode('utf-8'))