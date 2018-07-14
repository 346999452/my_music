#!usr/bin/env python
#-*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: forms
    @time: 2017/11/18

"""
from .models import *
from django.forms import ModelForm

''' 用户评论数据 '''
class user_comment_form(ModelForm):
    class Meta:
        model = user_comment
        fields = ['movie_id', 'user_id', 'comment', 'comment_time']

class likes_form(ModelForm):
    class Meta:
        model = likes
        fields = ['movie_id', 'comment_user_id','comment_time', 'user_id']

class barrage_form(ModelForm):
    class Meta:
        model = barrage
        fields = ['movie_id', 'value', 'color', 'time']