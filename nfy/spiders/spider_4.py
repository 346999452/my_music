#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_4
    @date: 2018/06/19
    
"""

# ! usr/bin/env python
# -*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_1
    @date: 2018/06/15

"""
from scrapy import Spider

class exam_spider(Spider):
    name = 'exam'

    ''' 设置爬取范围 '''
    # allowed_domains = ['163.com']

    start_urls = [
        'http://39.106.179.219/ac/lala',
    ]

    def parse(self, response):
        print(response.body.decode('utf-8'))