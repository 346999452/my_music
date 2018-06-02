# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: spider
    @time: 2018/05/06
    
"""
from scrapy import Spider, Request
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
            item['list_id'] = info[1]
            yield item

        new_cd = response.xpath('//ul[@class="f-cb roller-flag"]/li')
        for i in new_cd[: 10]:
            item = new_item()
            item['img'] = i.xpath('./div/img/@data-src').extract_first()
            item['name'] = i.xpath('./div/a[@class="msk"]/@title').extract_first()
            item['album_id'] = i.xpath('./div/a[@class="icon-play f-alpha f-fr"]/@data-res-id').extract_first()
            item['artist'] = i.xpath('./p[@class="tit f-thide"]/@title').extract_first()
            yield item

        rank = response.xpath('//div[@class="n-bilst"]/dl/dd/ol/li')
        category = ['云音乐飙升榜', '云音乐新歌榜', '抖音排行榜']
        for i in range(len(rank)):
            item = rank_item()
            item['name'] = rank[i].xpath('./a/text()').extract_first()
            item['song_id'] = rank[i].xpath('./div/a/@data-res-id').extract_first()
            item['rank'] = i % 10 + 1
            item['category'] = category[i // 10]
            yield item

        singer = response.xpath('//ul[@class="n-enter f-cb"]/li')
        for i in singer:
            item = singer_item()
            item['singer'] = i.xpath('./a/div[@class="ifo"]/h4/span/text()').extract_first()
            item['identity'] = i.xpath('./a/div[@class="ifo"]/p/text()').extract_first()
            href = i.xpath('./a/@href').extract_first()
            item['singer_id'] = re.findall(re.compile(r'(\d+)'), href)[0]
            item['img'] = i.xpath('./a/div[@class="head"]/img/@src').extract_first()
            item['category'] = '歌手'
            yield item

        hot_charac = response.xpath('//ul[@class="n-hotdj f-cb"]/li')
        for i in hot_charac:
            item = singer_item()
            item['img'] = i.xpath('./a/img/@data-src').extract_first()
            href = i.xpath('./div/p/a/@href').extract_first()
            item['singer_id'] = re.findall(re.compile(r'(\d+)'), href)[0]
            item['singer'] = i.xpath('./div/p/a/text()').extract_first()
            item['identity'] = i.xpath('./div/p[@class="f-thide s-fc3"]/text()').extract_first()
            item['category'] = '主播'
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
            item = lunbo_item()
            item['img'] = i[0]
            item['url'] = url
            yield item
        yield Request(url='http://music.163.com/discover/toplist?id=3778678', callback=self.parse_hot_music)

    def parse_hot_music(self, response):
        num = 0
        for i in response.xpath('//ul[@class="f-hide"]/li')[: 10]:
            num += 1
            item = rank_item()
            id = re.findall(re.compile(r'(\d+)'), i.xpath('./a/@href').extract_first())[0]
            item['song_id'] = id
            item['name'] = i.xpath('./a/text()').extract_first()
            item['rank'] = num
            item['category'] = '云音乐热歌榜'
            yield item