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
def logout(request):
    Yun_Music().logout()
    response = HttpResponseRedirect('/')
    response.delete_cookie('username')
    response.set_cookie('id')
    return response

def my_page(request):
    # id = request.COOKIES.get('id', None)
    # if id:
    #     info = Yun_Music().user_detail(id)
    #     dict = {
    #         'info': info[0],
    #         'create': info[1],
    #         'collec': info[2],
    #         'login': True
    #     }
    #     return render(request, 'user.html', Methods.add_username(request, dict))
    # else:
    #     dict = {'login': False}
    return render(request, 'template.html')



"""
    ——————————————————————————————————————————————————————————————————————————
    CBV
"""
from django.views import View
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
        try:
            info = self.playlist_detail(id)
            self.dict['info'] = info[0]
            self.dict['music_list'] = info[1]
            self.dict['hot_playlist'] = info[2]
            self.dict['user'] = info[3]
        except:
            return render(request, 'template.html')
        return render(request, 'music_list.html', self.add_username(request, self.dict))

    def post(self, request):
        pass

class artist(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.dict = {}

    def get(self, request):
        id = request.GET.get('id')
        category = request.GET.get('cat')
        info = self.artist_detail(id, category)
        self.dict['info'] = info[0]
        self.dict['detail'] = info[1]
        self.dict['cat'] = category
        return render(request, 'artist.html', self.add_username(request, self.dict))

    def post(self, request):
        pass

class rank(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.dict = {}

    def get(self, request):
        return render(request, 'template.html')

    def post(self, request):
        pass

class dj(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.dict = {}

    def get(self, request):
        return render(request, 'template.html')

    def post(self, request):
        pass

class user(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.dict = {}

    def get(self, request):
        id = request.GET.get('id')
        info = self.user_detail(id)
        self.dict['info'] = info[0]
        self.dict['create'] = info[1]
        self.dict['collec'] = info[2]
        return render(request, 'user.html', self.add_username(request, self.dict))

    def post(self, request):
        pass

class login(View, Yun_Music):
    def __init__(self):
        View.__init__(self)
        Yun_Music.__init__(self)
        self.dict = {
            'title': '登录',
            'year': datetime.now().year,
        }

    def get(self, request):
        return render(request, 'login.html', self.add_username(request, self.dict))

    def post(self, request):
        loginname = request.POST.get('loginname')
        password = request.POST.get('password')
        state, info = self.login(loginname, password)
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
            return render(request, 'login.html', Methods.add_username(request, self.dict))