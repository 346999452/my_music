# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: views
    @time: 2018/04/05

"""

from django.shortcuts import render, HttpResponseRedirect
from other_class.methods import Methods
from other_class.yun_music import Yun_Music
# Create your views here.

"""
    ——————————————————————————————————————————————————————————————————————————
    FBV
"""

def rank(request):
    return

def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('username')
    return response


"""
    ——————————————————————————————————————————————————————————————————————————
    CBV
"""
from django.views import View
from .forms import *
from datetime import datetime
from urllib.request import quote

class home(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.info = self.get_index()
        self.dict = {
                'new_song_list': self.info[1],
                'up_song_list': self.info[0],
                'original_song_list':self.info[2],
                'hot_song_list': self.get_top_10('云音乐热歌榜'),
                'singer_list': self.info[3],
                'popular_anchor': self.info[4],
                'play_list': self.info[5],
                'album_list': self.info[7],
                'lunbo_list': self.info[6]
            }

    def get(self, request):
        self.dict['commend'] = True
        if request.GET.get('play_list'):
            self.dict['play_list'] = self.get_play_list(request.GET.get('play_list'))[0][: 10]
            self.dict['commend'] = False
        return render(request, 'index.html', self.add_username(request, self.dict))

    def post(self, request):
        return

class play_music(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.info = self.get_index()
        self.dict = {}

    def get(self, request):
        id = request.GET.get('id')
        info = self.song_detail(id)
        play_music_page = self.get_play_music(id)
        list_name = {
            'name': info.get('name'),
            'id': info.get('id'),
            'artist_name': info['artists'][0]['name'],
            'artist_id': info['artists'][0]['id'],
            'album_name': info['album']['name'],
            'album_id': info['album']['id'],
            'album_img': info['album']['picUrl']
        }
        self.dict['src'] = self.get_music_src(id)
        self.dict['lyric'] = self.get_lyric(id)
        self.dict['info'] = list_name
        self.dict['play_list']= play_music_page[0]
        self.dict['similar_music'] = play_music_page[1]
        return render(request, 'music.html', self.add_username(request, self.dict))

    def post(self, request):
        pass

class play_list(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.dict = {}

    def get(self, request):
        categogy = request.GET.get('cat')
        info = self.get_play_list(categogy)
        self.dict['play_list'] = info[0]
        self.dict['category'] = info[1]
        return render(request, 'play_list.html', self.add_username(request, self.dict))

    def post(self, request):
        pass


class album(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.dict = {}

    def get(self, request):
        id = request.GET.get('id')
        info = self.album_detail(id)
        self.dict['info'] = info[0]
        self.dict['user'] = info[1]
        self.dict['album'] = info[2]
        self.dict['music'] = info[3]
        return render(request, 'album.html', self.add_username(request, self.dict))

    def post(self, request):
        pass

class music_list(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.dict = {}

    def get(self, request):
        id = request.GET.get('id')
        info = self.playlist_detail(id)
        self.dict['info'] = info[0]
        self.dict['music_list'] = info[1]
        self.dict['hot_playlist'] = info[2]
        self.dict['user'] = info[3]
        return render(request, 'music_list.html', self.add_username(request, self.dict))

    def post(self, request):
        pass

class artist(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)

    def get(self, request):
        id = request.GET.get('id')
        pass

    def post(self, request):
        pass

class my_collec(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)

    def get(self, request):
        username = request.COOKIES.get('username', None)
        if username:
            pass
        else:
            pass
        pass

    def post(self, request):
        pass

class register(View):
    def __init__(self):
        View.__init__(self)
        self.dict = {}

    def get(self, request):
        return render(request, 'register.html', Methods.add_username(request, self.dict))

    def post(self, request):
        usr = user_form(request.POST)
        if usr.is_valid():
            loginname = Methods.hash(usr.cleaned_data['loginname'])
            try:
                user.objects.get(loginname=loginname)
                self.dict['user_exit'] = True
                return render(request, 'register.html', Methods.add_username(request, self.dict))
            except:
                user(
                    username=usr.cleaned_data['username'],
                    loginname=loginname,
                    password=Methods.hash(usr.cleaned_data['password'])
                ).save()
                return HttpResponseRedirect('/ac/login')
        else:
            self.dict['str_error'] = True
            return render(request, 'register.html', Methods.add_username(request, self.dict))

class login(View):
    def __init__(self):
        View.__init__(self)
        self.dict = {
            'title': '登录',
            'year': datetime.now().year,
        }

    def get(self, request):
        return render(request, 'login.html', Methods.add_username(request, self.dict))

    def post(self, request):
        loginname = request.POST.get('loginname')
        password = request.POST.get('password')
        try:
            a = user.objects.get(loginname=Methods.hash(loginname), password=Methods.hash(password))
            response = HttpResponseRedirect('/')

            """ 
                设置cookie值，这里将cookie有效时间设置为3600秒, 即一小时 
                quote: 将url编码不支持的字符（例如中文）转换成url支持的编码格式， urlencode
            """
            response.set_cookie('username', quote(a.username), 3600)
            return response
        except:
            self.dict['key_error'] = True
            return render(request, 'login.html', Methods.add_username(request, self.dict))