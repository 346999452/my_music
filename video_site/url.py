#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: url
    @date: 2018/07/03
    
"""

from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^$', index.as_view(), name='js'),
    url('^cat/', cat, name='cat'),
    url('^search/', search.as_view(), name='search'),
    url(r'^like$', like, name='like'),
    url('^unlike/', unlike, name='unlike'),
    url('^shanchu/', shanchu, name='delete'),
    url(r'^shi$', shi),
    url(r'^play/$', play.as_view())
]