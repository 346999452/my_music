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
    url(r'^home$', index.as_view()),
    url(r'^cat/', cat),
    url(r'^search/', search.as_view()),
    url(r'^like/$', like),
    url(r'^unlike/$', unlike),
    url(r'^delete/$', delete),
    url(r'^$', home.as_view(), name='video'),
    url(r'^play/$', play.as_view()),
    url(r'^barrage/$', danmu.as_view())
]