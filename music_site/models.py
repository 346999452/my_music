# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: models
    @time: 2018/04/05

"""

from django.db.models import Model, CharField, IntegerField, DateTimeField

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
    name = CharField(max_length=200)
    rank = IntegerField()
    category = CharField(max_length=20)

''' 歌单分类 '''
class category_model(Model):
    '''
        category: 歌单大分类
        cat: 歌单小分类
    '''
    category = CharField(max_length=10)
    cat = CharField(max_length=10)

''' 歌单信息 '''
class play_list_model(Model):
    '''
        name: 歌单名
        id: 歌单id
        img: 图片链接
        author: 用户
        author_id: 用户id
    '''
    name = CharField(max_length=50)
    play_list_id = CharField(max_length=20)
    img = CharField(max_length=200)
    author = CharField(max_length=50)
    author_id = CharField(max_length=20)
    category = CharField(max_length=10)

''' 榜单信息 '''
class top_list_model(Model):
    '''
        top_list_id: 排行榜id
        name: 排行榜名
        img: 图片链接
        last_change: 最近更新
        cycle: 更新周期
    '''
    top_list_id = CharField(max_length=20)
    name = CharField(max_length=30)
    img = CharField(max_length=400)
    last_change = CharField(max_length=20)
    cycle = CharField(max_length=20)

''' ip反爬虫库 '''
class robot_killer(Model):
    '''
        ip: IP地址
        visits: 请求次数
        time: 第一次发起请求的时间
    '''
    id = IntegerField(primary_key=True)
    ip = CharField(max_length=16)    #IP地址
    visits = IntegerField()          #请求次数
    time = DateTimeField()           #第一次发起请求的时间

    class Meta:
        db_table = 'robotkiller'