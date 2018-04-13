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
    url(r'^music_list/', music_list.as_view(), name='music_list'),
    url(r'^artist/$', artist.as_view(), name='artist'),
    url(r'^login/$', login.as_view(), name='login'),
    url(r'^rank/$', rank.as_view(), name='rank'),
    url(r'^user/$', user.as_view(), name='user'),
    url(r'dj/$', dj.as_view(), name='dj'),
    url(r'^my_page', my_page, name='my_page')
]