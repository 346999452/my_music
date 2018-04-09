# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: models
    @time: 2018/04/05

"""

from django.db import models

''' 用户模型 '''
class user(models.Model):
    username = models.CharField(max_length=32)
    loginname = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __str__(self):
        return '{} | {}'.format(self.username, self.password)

''' 单曲信息 '''
class music_info(models.Model):
    music_id = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=50)
    pic_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

''' 专辑信息 '''
class album_info(models.Model):
    album_id = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=50)
    pic_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

''' 歌单信息 '''
class playlist_info(models.Model):
    playlist_id = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=50)
    pic_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

''' 收藏的单曲 '''
class music_collec(models.Model):
    loginname = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    music_id = models.CharField(max_length=15)

''' 收藏的专辑 '''
class album_collec(models.Model):
    loginname = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    album_id = models.CharField(max_length=15)

''' 收藏的歌单 '''
class playlist_collec(models.Model):
    loginname = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    playlist_id = models.CharField(max_length=15)