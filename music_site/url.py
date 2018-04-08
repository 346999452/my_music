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
    url(r'^music/$', logout, name='music'),
    url(r'^play_list/$', logout, name='play_list'),
    url(r'^album/$', logout, name='album'),
    url(r'^rank/$', rank, name='rank'),
    url(r'^login/$', login.as_view(), name='login'),
    url(r'^register/$', register.as_view(), name='regist'),
]