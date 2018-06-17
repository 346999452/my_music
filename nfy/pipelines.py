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

class NfyPipeline(object):

    def __init__(self, host, user, password, db, port, charset):
        import pymysql
        self.db = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port,
            charset=charset
        )
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        if spider.name == 'top_list':
            with open('{}json/{}.json'.format(Methods.absolute_path, item['list_name']), 'w', encoding='utf-8') as f:
                f.write(item['rank_info'])
        else:
            try:
                item.save()
            except:
                pass
        return item

    def open_spider(self, spider):
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