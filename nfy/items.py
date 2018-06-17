# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: __init__
    @time: 2018/05/06

    定义数据结构，类似于django框架中的models
    see http://doc.scrapy.org/en/latest/topics/items.html
"""

from scrapy_djangoitem import DjangoItem
from music_site.models import *
from scrapy import Item, Field

class lunbo_item(DjangoItem):
    django_model = lunbo_model

class commend_item(DjangoItem):
    django_model = commend_model

class new_item(DjangoItem):
    django_model = new_model

class singer_item(DjangoItem):
    django_model = singer_model

class rank_item(DjangoItem):
    django_model = rank_model

# class user_item(DjangoItem):
#     django_model = user_model
#
# class collec_item(DjangoItem):
#     django_model = collec_model

class top_list_item(Item):
    '''
        list_name: 榜单名
        rank_info: 排行信息
    '''
    list_name = Field()
    rank_info = Field()

class play_list_item(DjangoItem):
    django_model = play_list_model

class category_item(DjangoItem):
    django_model = category_model