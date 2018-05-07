# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: __init__
    @time: 2018/05/06

    定义数据结构，类似于django框架中的models
    see http://doc.scrapy.org/en/latest/topics/items.html
"""

from scrapy import Item, Field

''' 轮播图结构 '''
class NfyItem(Item):
    img = Field()
    url = Field()

''' 热门推荐结构 '''
class commend_item(Item):
    id = Field()
    title = Field()
    index = Field()
    category = Field()
    img = Field()

''' 新碟上架 '''
class new_item(Item):
    id = Field()
    name = Field()
    artist = Field()
    img = Field()

''' 入驻歌手及热门主播的数据结构 '''
class singer_item(Item):
    singer = Field()
    identity = Field()
    img = Field()
    id = Field()
    filename = Field()

''' 榜单信息 '''
class rank_item(Item):
    id = Field()
    name = Field()
    rank = Field()
    filename = Field()

if __name__ == '__main__':
    nfy = NfyItem()
    nfy['url'] = 'nfy'
    print(nfy.get('url'))