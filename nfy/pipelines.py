# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: __init__
    @time: 2018/05/06

    管道
    一般用于存储数据为文件或者入库
    See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
from other_class.methods import Methods
import pymysql
from nfy.items import *

class NfyPipeline(object):

    def __init__(self, host, user, password, db, port, charset):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.charset = charset

    def process_item(self, item, spider):
        if isinstance(item, top_list_item):
            with open('{}json/{}.json'.format(Methods.absolute_path, item['list_name']), 'w', encoding='utf-8') as f:
                f.write(item['rank_info'])
        else:
            try:
                item.save()
            except:
                pass
        return item

    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            port=self.port,
            charset=self.charset
        )
        self.cur = self.db.cursor()

        def truncate(table):
            try:
                self.cur.execute('truncate table music_site_' + table + '_model')
                self.db.commit()
            except:
                self.db.rollback()

        if spider.name == 'nfy':
            truncate('commend')
            truncate('lunbo')
            truncate('new')
            truncate('rank')
            truncate('singer')
        elif spider.name == 'play_list':
            truncate('category')
            truncate('play_list')
        elif spider.name == 'top_list':
            truncate('top_list')

    def close_spider(self, spider):
        self.db.close()

    @classmethod
    def from_crawler(cls, crawler):
        conf = crawler.settings.get('MYSQL_DATABASE')
        return cls(
            host=conf.get('HOST'),
            user=conf.get('USER'),
            password=conf.get('PASSWORD'),
            db=conf.get('DB'),
            port=conf.get('PORT'),
            charset=conf.get('CHARSET')
        )

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

'''
    scrapy提供的专门处理下载的Pipeline，包括文件下载和图片下载
    下载文件和图片的原理和抓取页面的原理一样，因此下载过程支持异步和多线程，下载十分高效
    
    内置的ImagesPipeline会默认获取item的image_urls字段，并认为该字段是一个列表形式，他会遍历
item的image_urls字段，然后取出每个url进行图片下载

    但现在生成的item的图片链接字段并不是image_urls字段表示的，也不是列表形式，而是单个url
    所以为了实现下载，我们需要重新定义部分逻辑，即要重新定义ImagesPipeline，重写几个方法
'''
class ImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        yield Request(item['url'])