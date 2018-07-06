#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_5
    @date: 2018/07/04
    
"""

from scrapy import Spider, Request
from nfy.items import movie_item
import json

class MySpider(Spider):

    name = 'video'

    allowed_domains = ['kaiyanapp.com']

    start_urls = [
        'http://baobab.kaiyanapp.com/api/v4/tabs/selected',
    ]

    def parse(self, response):
        content = json.loads(response.body.decode('utf-8'))
        for i in content.get('itemList'):
            if i.get('type') == 'video':
                i = i.get('data')
                item = movie_item()
                item['title'] = i.get('title')
                item['category'] = i.get('category')
                item['img'] = i.get('cover').get('homepage')
                item['slogan'] = i.get('slogan')
                item['home_page'] = i.get('cover').get('homepage')
                item['play_url'] = i.get('playUrl')
                item['id'] = i.get('id')
                yield item

        next_url = content.get('nextPageUrl')
        if next_url:
            yield Request(next_url, callback=self.parse)