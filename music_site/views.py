# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: views
    @time: 2018/04/05

"""

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from other_class.yun_music import Yun_Music
from .models import *
from django.forms.models import model_to_dict
import json
from urllib.request import unquote
from django.utils import timezone

# Create your views here.

ym = Yun_Music()

max_visits = 100
min_seconds = 600

'''
    用于将数据库model转换成dict形式
'''
def change(model, category=None, ori=None, limit=None):
    if category:
        obj = model.objects.filter(category=category)
    else:
        obj = model.objects.all()
    if ori is not None and limit:
        return [model_to_dict(i) for i in obj[ori: ori + limit]]
    return [model_to_dict(i) for i in obj]

''' 获得cookie中的username值 '''
def add_username(request, dict):
    username = request.COOKIES.get('username', None)
    if username:
        ''' unquote: url解码 '''
        dict['username'] = unquote(username)
    else:
        dict['error'] = True
    return dict

"""
    ——————————————————————————————————————————————————————————————————————————
    FBV
"""

''' 用于测试scrapy爬虫携带的信息 '''
def lala(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return HttpResponse({
        request.environ['HTTP_USER_AGENT'] + '<br>' + ip + '<br>' + json.dumps(request.COOKIES)
    })

def logout(request):
    Yun_Music().logout()
    response = HttpResponseRedirect('/')
    response.delete_cookie('username')
    response.delete_cookie('id')
    return response

def my_page(request):
    id = request.COOKIES.get('id', None)
    if id:
        info = ym.user_detail(id)
        return render(request, 'user.html', add_username(request, {
            'info': info[0],
            'create': info[1],
            'collec': info[2]
        }))
    else:
        return HttpResponseRedirect('/ac/login')

def search(request):
    key_word = request.POST.get('key_word')
    return render(request, 'result.html', add_username(request, {'music_list': ym.search_song(key_word)}))

'''
    ip反爬函数
'''
def filter_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        user_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        user_ip = request.META['REMOTE_ADDR']

    try:
        record = robot_killer.objects.using('robotkiller').get(ip=user_ip)
    except robot_killer.DoesNotExist:
        robot_killer.objects.using('robotkiller').create(ip=user_ip, visits=1, time=timezone.now())
        return

    passed_seconds = (timezone.now() - record.time).seconds

    if record.visits > max_visits and passed_seconds < min_seconds:
        raise Exception('user ip banned.')
    else:
        if passed_seconds < min_seconds:
            record.visits = record.visits + 1
            record.save()
        else:
            record.visits = 1
            record.time = timezone.now()
            record.save()

"""
    ——————————————————————————————————————————————————————————————————————————
    CBV
"""
from django.views import View
from datetime import datetime
from urllib.request import quote

class home(View):

    def get(self, request):
        return render(request, 'index.html', add_username(request, {'lunbo': change(lunbo_model)}))

    def post(self, request):
        if request.POST.get('info'):
            return HttpResponse(json.dumps({
                'commend': change(commend_model),
                'new_cd': change(new_model),
                'up_rank': change(rank_model, '云音乐飙升榜'),
                'new_rank': change(rank_model, '云音乐新歌榜'),
                'douyin_rank': change(rank_model, '抖音排行榜'),
                'hot_rank': change(rank_model, '云音乐热歌榜'),
                'singer': change(singer_model, '歌手'),
                'charac': change(singer_model, '主播')
            }))
        else:
            return search(request)

class play_music(View):

    def get(self, request):
        id = request.GET.get('id')
        try:
            info = ym.song_detail(id)
            list_name = {
                'name': info.get('name'),
                'id': info.get('id'),
                'artist_name': info['artists'][0]['name'],
                'artist_id': info['artists'][0]['id'],
                'album_name': info['album']['name'],
                'album_id': info['album']['id'],
                'album_img': info['album']['picUrl']
            }
            dict = {
                'src': ym.get_music_src(id),
                'info': list_name,
                'id': id
            }
            return render(request, 'play_music.html', add_username(request, dict))
        except:
            return render(request, 'template.html', add_username(request, {}))

    def post(self, request):
        id = request.POST.get('id')
        if id:
            info = ym.song_detail(id)
            play_music_page = ym.get_play_music(id)
            return HttpResponse(json.dumps({
                'lyric': ym.get_lyric(id),
                'img_src': ym.get_background(info.get('name')),
                'play_list': play_music_page[0],
                'similar_music': play_music_page[1]
            }))
        else:
            return search(request)

class play_list(View):

    def get(self, request):
        return render(request, 'play_list.html', add_username(request, {}))

    def post(self, request):
        try:
            filter_ip(request)
        except Exception as e:
            if e == 'user ip banned.':
                return render(request, 'template.html')
        cat = request.POST.get('cat')
        if cat:
            ori = request.POST.get('ori')
            return HttpResponse(json.dumps({
                'data': change(play_list_model, cat, int(ori), 36),
                'max_page': (play_list_model.objects.filter(category=cat).count() - 1) // 36
            }))
        return search(request)

class album(View):

    def get(self, request):
        id = request.GET.get('id')
        info = ym.album_detail(id)
        return render(request, 'album.html', add_username(request, {
            'info': info[0],
            'user': info[1],
            'album': info[2],
            'music': info[3]
        }))

    def post(self, request):
        return search(request)

class music_list(View):

    def get(self, request):
        id = request.GET.get('id')
        try:
            info = ym.playlist_detail(id)
            dict = {
                'info': info[0],
                'music_list': info[1],
                'hot_playlist': info[2],
                'user': info[3],
                'id': id
            }
        except:
            return render(request, 'template.html')
        return render(request, 'music_list.html', add_username(request, dict))

    def post(self, request):
        id = request.POST.get('id')
        if id:
            info = ym.playlist_detail(id)
            return HttpResponse(json.dumps({
                'info': info[0],
                'music_list': info[1],
                'hot_playlist': info[2],
                'user': info[3]
            }))
        else:
            return search(request)

class artist(View):

    def get(self, request):
        id = request.GET.get('id')
        category = request.GET.get('cat')
        info = ym.artist_detail(id, category)
        return render(request, 'artist.html', add_username(request, {
            'info': info[0],
            'detail': info[1],
            'cat': category
        }))

    def post(self, request):
        return search(request)

class top_list(View):

    def get(self, request):
        top_list = top_list_model.objects.all()
        return render(request, 'top_list.html', add_username(request, {'charac': top_list[: 4], 'global': top_list[4:]}))

    def post(self, request):
        id = request.POST.get('id')
        if id:
            top_list = top_list_model.objects.get(top_list_id=str(id))
            with open('{}json/{}.json'.format(ym.absolute_path, top_list.name), 'r', encoding='utf-8') as f:
                return HttpResponse(json.dumps({
                    'img': top_list.img,
                    'songs': f.read(),
                    'title': top_list.name,
                    'last': top_list.last_change,
                    'cycle': top_list.cycle
                }))
        else:
            return search(request)

class dj(View):

    def get(self, request):
        id = request.GET.get('id')
        return HttpResponseRedirect('/ac/music/?id={}'.format(ym.dj_detail(id)[0].get('music_id')))

    def post(self, request):
        return search(request)

class user(View):

    def get(self, request):
        id = request.GET.get('id')
        info = ym.user_detail(id)
        return render(request, 'user.html', add_username(request, {
            'info': info[0],
            'create': info[1],
            'collec': info[2]
        }))

    def post(self, request):
        return search(request)

class mv(View):

    def get(self, request):
        return render(request, 'mv.html', add_username(request, {
            'lala': 'http://v4.music.126.net/20180427183740/9eb6d8fbc42eef1f4ac5b9c0b8b67ac6/web/cloudmusic/mv/20171225021126/5eab069b-9681-44e0-8db4-3cbcd2d87d6d/c251f005d2fcc28b8c5013ece7a70a93.mp4',
        }))

    def post(self, request):
        return search(request)

class login(View):

    def __init__(self):
        super(login, self).__init__()
        self.dict = {
            'title': '登录',
            'year': datetime.now().year,
        }

    def get(self, request):
        return render(request, 'login.html', add_username(request, self.dict))

    def post(self, request):
        if request.POST.get('login'):
            loginname = request.POST.get('loginname')
            password = request.POST.get('password')
            state, info = ym.login(loginname, password)
            if state:
                response = HttpResponseRedirect('/')
                """
                    设置cookie值，这里将cookie有效时间设置为3600秒, 即一小时
                    quote: 将url编码不支持的字符（例如中文）转换成url支持的编码格式， urlencode
                """
                response.set_cookie('username', quote(info[1]), 3600)
                response.set_cookie('id', info[0], 3600)
                return response
            else:
                self.dict['key_error'] = info
                return render(request, 'login.html', add_username(request, self.dict))
        else:
            return search(request)