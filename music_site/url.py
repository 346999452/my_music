# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: url
    @time: 2018/04/05
    
"""

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^logout/$', logout, name='logout'),
    url(r'^music/$', play_music.as_view(), name='music'),
    url(r'^play_list/$', play_list.as_view(), name='play_list'),
    url(r'^album/$', album.as_view(), name='album'),
    url(r'^artist/$', artist.as_view(), name='artist'),
    url(r'^login/$', login.as_view(), name='login'),
    url(r'^register/$', register.as_view(), name='regist'),
]