# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: models
    @time: 2018/04/05

"""

from django.db.models import Model, CharField, IntegerField

''' 轮播图结构 '''
class lunbo_model(Model):
    '''
        img: 图片资源链接
        url: 跳转资源链接
    '''
    img = CharField(max_length=400)
    url = CharField(max_length=400)

''' 热门推荐结构 '''
class commend_model(Model):
    '''
        list_id: 歌单/电台id
        title: 标题
        index: 索引——music_list/dj
        category: 类别——歌单/电台节目
        img: 图片资源链接
    '''
    list_id = CharField(max_length=30)
    title = CharField(max_length=200)
    index = CharField(max_length=20)
    category = CharField(max_length=10)
    img = CharField(max_length=400)

''' 新碟上架 '''
class new_model(Model):
    '''
        album_id: 专辑id
        name: 专辑名
        artist: 作者
        img: 图片资源链接
    '''
    album_id = CharField(max_length=30)
    name = CharField(max_length=50)
    artist = CharField(max_length=50)
    img = CharField(max_length=400)

''' 入驻歌手及热门主播的数据结构 '''
class singer_model(Model):
    '''
        singer_id: 音乐人id
        singer: 歌手
        identity: 身份介绍
        category: 歌手/主播
        img: 图片资源链接
    '''
    singer_id = CharField(max_length=30)
    singer = CharField(max_length=50)
    identity = CharField(max_length=200)
    category = CharField(max_length=50)
    img = CharField(max_length=400)

''' 榜单信息 '''
class rank_model(Model):
    '''
        song_id: 音乐id
        name: 音乐名
        rank: 排行
        category: 哪个榜单
    '''
    song_id = CharField(max_length=30)
    name = CharField(max_length=50)
    rank = IntegerField()
    category = CharField(max_length=20)

