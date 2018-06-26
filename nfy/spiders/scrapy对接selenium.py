#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: scrapy对接selenium
    @date: 2018/06/25
    
"""
from scrapy import Spider, Request
from urllib.request import quote

class exam_spider(Spider):
    name = 'selenium'

    ''' 设置爬取范围 '''
    allowed_domains = ['163.com']

    start_urls = [

    ]

    def parse(self, response):
        print(response.body.decode('utf-8'))