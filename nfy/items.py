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