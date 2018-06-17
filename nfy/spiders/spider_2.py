#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_2
    @date: 2018/06/15
    
"""

from scrapy import Spider, Request
from nfy.items import top_list_item

class rank_spider(Spider):

    name = 'top_list'

    allowed_domains = ['163.com']

    start_urls = ['http://music.163.com/discover/toplist']

    def parse(self, response):
        top_list = response.xpath('//ul[@class="f-cb"]/li')
        for i in top_list:
            yield Request('http://music.163.com' + i.xpath('./div/div/a[@class="avatar"]/@href').extract_first(), callback=self.detail_parse)

    def detail_parse(self, response):
        item = top_list_item()
        item['list_name'] = response.xpath('//h2[@class="f-ff2"]/text()').extract_first()
        item['rank_info'] = response.xpath('//textarea[@id="song-list-pre-data"]/text()').extract_first()
        yield item