#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider_3
    @date: 2018/06/16
    
"""

from scrapy import Spider, Request
from nfy.items import *
import re

class play_list_spider(Spider):

    name = 'play_list'

    allowed_domains = ['163.com']

    start_urls = ['http://music.163.com/discover/playlist/']

    def parse(self, response):
        yield Request('http://music.163.com/discover/playlist/', self.cat_parse)
        theme = response.xpath('//dl[@class="f-cb"]')
        for i in theme:
            # category = i.xpath('./dt/text()').extract_first()
            for j in i.xpath('./dd/a'):
                # item = category_item()
                # item['category'] = category
                # item['cat'] = j.xpath('./text()').extract_first()
                # yield item
                yield Request('http://music.163.com/discover/playlist/?cat=' + j.xpath('./text()').extract_first(), self.cat_parse)

    def cat_parse(self, response):

        current_category = response.xpath('//span[@class="f-ff2 d-flag"]/text()').extract_first()
        play_list = response.xpath('//ul[@class="m-cvrlst f-cb"]/li')
        for i in play_list:
            item = play_list_item()
            item['img'] = i.xpath('./div/img/@src').extract_first()
            item['name'] = i.xpath('./p/a/@title').extract_first()
            item['play_list_id'] = re.findall(re.compile(r'(\d+)'), i.xpath('./p/a/@href').extract_first())[0]
            item['author'] = i.xpath('./p/a[@class="nm nm-icn f-thide s-fc3"]/text()').extract_first()
            item['author_id'] = re.findall(re.compile(r'(\d+)'), i.xpath('./p/a[@class="nm nm-icn f-thide s-fc3"]/@href').extract_first())[0]
            item['category'] = current_category
            yield item

        link = response.xpath('//div[@id="m-pl-pager"]/div/a').extract()[-1]
        href = re.findall(re.compile(r'href="([^"]+)'), link)[0]
        if href != 'javascript:void(0)':
            new_href = re.sub('amp;', '', href)
            yield Request('http://music.163.com' + new_href, callback=self.cat_parse)