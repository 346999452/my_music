# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider
    @time: 2018/05/06
    
"""
from scrapy import Spider
from nfy.items import *
import re

class MySpider(Spider):

    name = 'nfy'

    ''' 设置爬取范围 '''
    allowed_domains = ['163.com']

    start_urls = [
        'http://music.163.com/discover',
    ]

    def parse(self, response):

        commend = response.xpath('//ul[@class="m-cvrlst f-cb"]/li')
        for i in commend:
            item = commend_item()
            item['img'] = i.xpath('./div/img/@src').extract_first()
            item['title'] = i.xpath('./div/a/@title').extract_first()
            href = i.xpath('./div/a/@href').extract_first()
            info = re.findall(re.compile(r'/([a-z]+)\?id=(\d+)'), href)[0]
            item['index'] = 'music_list' if info[0] == 'playlist' else 'dj'
            item['category'] = '电台节目' if info[0] == 'dj' else '歌单'
            item['id'] = info[1]
            yield item

        new_cd = response.xpath('//ul[@class="f-cb roller-flag"]/li')
        for i in new_cd[: 10]:
            item = new_item()
            item['img'] = i.xpath('./div/img/@data-src').extract_first()
            item['name'] = i.xpath('./div/a[@class="msk"]/@title').extract_first()
            item['id'] = i.xpath('./div/a[@class="icon-play f-alpha f-fr"]/@data-res-id').extract_first()
            item['artist'] = i.xpath('./p[@class="tit f-thide"]/@title').extract_first()
            yield item

        rank = response.xpath('//div[@class="n-bilst"]/dl/dd/ol/li')
        filename = ['file/fill_blank/40.txt', 'file/fill_blank/50.txt', 'file/fill_blank/60.txt']
        for i in range(len(rank)):
            item = rank_item()
            item['name'] = rank[i].xpath('./a/text()').extract_first()
            item['id'] = rank[i].xpath('./div/a/@data-res-id').extract_first()
            item['rank'] = i % 10 + 1
            item['filename'] = filename[i // 10]
            yield item

        singer = response.xpath('//ul[@class="n-enter f-cb"]/li')
        for i in singer:
            item = singer_item()
            item['singer'] = i.xpath('./a/div[@class="ifo"]/h4/span/text()').extract_first()
            item['identity'] = i.xpath('./a/div[@class="ifo"]/p/text()').extract_first()
            href = i.xpath('./a/@href').extract_first()
            item['id'] = re.findall(re.compile(r'(\d+)'), href)[0]
            item['img'] = i.xpath('./a/div[@class="head"]/img/@src').extract_first()
            item['filename'] = 'file/fill_blank/70.txt'
            yield item

        hot_charac = response.xpath('//ul[@class="n-hotdj f-cb"]/li')
        for i in hot_charac:
            item = singer_item()
            item['img'] = i.xpath('./a/img/@data-src').extract_first()
            href = i.xpath('./div/p/a/@href').extract_first()
            item['id'] = re.findall(re.compile(r'(\d+)'), href)[0]
            item['singer'] = i.xpath('./div/p/a/text()').extract_first()
            item['identity'] = i.xpath('./div/p[@class="f-thide s-fc3"]/text()').extract_first()
            item['filename'] = 'file/fill_blank/80.txt'
            yield item


        lunbo = response.xpath('//script[@type="text/javascript"]').extract()[1]
        li = ['song', 'album', 'mv']
        for i in re.findall(re.compile(r'picUrl : "([^"]+)",\nurl : "([^"]+)",'), lunbo):
            try:
                id = re.findall(re.compile('id=(\d+)'), i[1])[0]
                for j in li:
                    if re.search(re.compile(j), i[1]):
                        url = '/ac/{}/?id={}'.format('music' if j == 'song' else j, id)
                        break
                else:
                    url = i[1]
            except:
                url = i[1]
            item = NfyItem()
            item['img'] = i[0]
            item['url'] = url
            yield item

class Another_Spider(Spider):

    name = "mu163"

    ''' 设置爬取范围 '''
    allowed_domains = ['163.com']

    start_urls = [
        'http://music.163.com/discover/toplist?id=3778678',
    ]

    def parse(self, response):
        num = 0
        for i in response.xpath('//ul[@class="f-hide"]/li')[: 10]:
            num += 1
            item = rank_item()
            id = re.findall(re.compile(r'(\d+)'), i.xpath('./a/@href').extract_first())[0]
            item['id'] = id
            item['name'] = i.xpath('./a/text()').extract_first()
            item['rank'] = num
            item['filename'] = 'file/fill_blank/30.txt'
            yield item

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(MySpider)
    process.crawl(Another_Spider)
    process.start()



