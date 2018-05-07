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
from nfy.items import *

class NfyPipeline(object):

    ''' 热门推荐 '''
    def process_commend(self, item):
        template = '''
                    <li>
                      <div class="u-cover">
                        <img src="{}">
                        <a title="{}" href="/ac/{}?id={}" class="msk"></a>
                      </div>
                      <p class="dec">
                        <a title="{}" href="/ac/{}?id={}">{}</a>
                      </p>
                      <div class="author">{}</div>
                    </li>
                    '''
        new_temp = template.format(item['img'], item['title'], item['index'], item['id'],
                   item['title'], item['index'], item['id'], item['title'], item['category'])
        with open('file/10.txt', 'ab') as fp:
            fp.write(bytes(new_temp + '\n', encoding='utf-8'))

    ''' 新碟上架 '''
    def process_newcd(self, item):
        template = '''
                    <li>
                      <div class="u-cover">
                        <img src="{}">
                        <a title="{}" href="/ac/album?id={}" class="msk"></a>
                      </div>
                      <p class="dec">
                        <a title="{}" href="/ac/album?id={}">{}</a>
                      </p>
                      <div class="author">{}</div>
                    </li>
                    '''
        new_temp = template.format(item['img'], item['name'], item['id'], item['name'],
                                item['id'], item['name'], item['artist'])
        with open('file/20.txt', 'ab') as fp:
            fp.write(bytes(new_temp + '\n', encoding='utf-8'))

    ''' 榜单信息 '''
    def process_rank(self, item):
        template = '''
                    <li class="music-list-item">
                      <div class="title">
                        <div class="title_wrap">
                          <span class="rank">{}.</span>
                          <a href="/ac/music/?id={}" title="Refrain">{}</a>
                        </div>
                      </div>
                      <div class="info">
                        <span class="avatar"><p></p></span>
                      </div>
                    </li>
                    '''
        new_temp = template.format(item['rank'], item['id'], item['name'])
        with open(item['filename'], 'ab') as fp:
            fp.write(bytes(new_temp + '\n', encoding='utf-8'))

    ''' 入驻歌手 '''
    def process_singer(self, item):
        template = '''
                    <li class="artist-song">
                      <div class="avatar">
                        <img src="{}">
                      </div>
                      <div class="info">
                        <h3>{}</h3>
                        <p>{}</p>
                      </div>
                      <a href="/ac/user?id={}" title="{}" class="cover-link"></a>
                    </li>
                    '''
        new_temp = template.format(item['img'], item['singer'], item['identity'], item['id'],
                                   item['singer'])
        with open(item['filename'], 'ab') as fp:
            fp.write(bytes(new_temp + '\n', encoding='utf-8'))

    def process_lunbo(self, item):
        template = "var data = {" \
                   "title: ''," \
                   "pic: '" + item['img'] +"'," \
                   "url: '" + item['url'] + "'" \
                   "};" \
                   "sliderData.push(data);"
        with open('file/90.txt', 'ab') as fp:
            fp.write(bytes(template + '\n', encoding='utf-8'))

    def process_item(self, item, spider):
        if isinstance(item, NfyItem):
            self.process_lunbo(item)
        elif isinstance(item, commend_item):
            self.process_commend(item)
        elif isinstance(item, new_item):
            self.process_newcd(item)
        elif isinstance(item, rank_item):
            self.process_rank(item)
        elif isinstance(item, singer_item):
            self.process_singer(item)
        return item
