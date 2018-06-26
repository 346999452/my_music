#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_1
    @date: 2018/06/15
    
"""
from scrapy import Spider, Request
import json

class user_spider(Spider):

    name = 'user'

    ''' 设置爬取范围 '''
    allowed_domains = ['163.com']

    users = ['29879272', '100167517', '58426904', '93504818', '46998208',
             '278438485', '91239965', '324314596', '1611157', '2313954']

    def start_requests(self):
        for user in self.users:
            yield Request(url='http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=' + user, callback=self.parse)


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