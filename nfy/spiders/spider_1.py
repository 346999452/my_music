#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_1
    @date: 2018/06/15
    
"""
from scrapy import Spider
import json

class user_spider(Spider):

    name = 'user'

    ''' 设置爬取范围 '''
    allowed_domains = ['163.com']

    start_urls = [
        'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=29879272',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=100167517',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=58426904',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=93504818',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=46998208',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=278438485',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=91239965',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=324314596',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=1611157',
        # 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=2313954',
    ]

    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))['playlist']
        user_id = ''
        for i in data:
            user_id = i['userId']
            creator_id = i['creator']['userId']
            print(user_id)
            print(creator_id)

    def parse_json(self, response):
        pass