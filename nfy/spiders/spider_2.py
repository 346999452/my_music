#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_2
    @date: 2018/06/15
    
"""

from scrapy import Spider, Request
from nfy.items import *

class rank_spider(Spider):

    name = 'top_list'

    allowed_domains = ['163.com']

    start_urls = ['http://music.163.com/discover/toplist']

    def parse(self, response):
        top_list = response.xpath('//ul[@class="f-cb"]/li')
        for i in top_list:
            yield Request('http://music.163.com' + i.xpath('./div/div/a[@class="avatar"]/@href').extract_first(), callback=self.detail_parse)

    def detail_parse(self, response):
        item = top_list_info_item()
        info = response.xpath('//div[@class="m-info m-info-rank f-cb"]')
        item['img'] = info.xpath('./div[@class="cover u-cover u-cover-rank"]/img/@src').extract_first()
        item['name'] = info.xpath('//h2[@class="f-ff2"]/text()').extract_first()
        item['last_change'] = info.xpath('//span[@class="sep s-fc3"]/text()').extract_first().split('：')[-1]
        item['cycle'] = info.xpath('//span[@class="s-fc4"]/text()').extract_first()
        item['top_list_id'] = info.xpath('//a[@class="u-btni u-btni-add"]/@data-res-id').extract_first()
        yield item

        item = top_list_item()
        item['list_name'] = response.xpath('//h2[@class="f-ff2"]/text()').extract_first()
        item['rank_info'] = response.xpath('//textarea[@id="song-list-pre-data"]/text()').extract_first()
        yield item