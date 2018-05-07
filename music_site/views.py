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
    response.delete_cookie('id')
    return response

def my_page(request):
    id = request.COOKIES.get('id', None)
    if id:
        info = Yun_Music().user_detail(id)
        dict = {
            'info': info[0],
            'create': info[1],
            'collec': info[2]
        }
        return render(request, 'user.html', Methods.add_username(request, dict))
    else:
        return HttpResponseRedirect('/ac/login')

def search(request):
    key_word = request.POST.get('key_word')
    return render(request, 'result.html', Methods.add_username(request, {'music_list': Yun_Music().search_song(key_word)}))

"""
    ——————————————————————————————————————————————————————————————————————————
    CBV
"""
from django.views import View
from datetime import datetime
from urllib.request import quote

class home(View, Yun_Music):

    def get(self, request):
        # Yun_Music.__init__(self)
        # info = self.get_index()
        # dict = {
        #     'new_song_list': info[1],
        #     'up_song_list': info[0],
        #     'original_song_list': info[2],
        #     'hot_song_list': self.get_top_10('云音乐热歌榜'),
        #     'singer_list': info[3],
        #     'popular_anchor': info[4],
        #     'play_list': info[5],
        #     'album_list': info[7],
        #     'lunbo_list': info[6]
        # }
        return render(request, 'index_template.html', self.add_username(request, {}))

    def post(self, request):
        return search(request)

class play_music(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        id = request.GET.get('id')
        try:
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
            dict = {
                'src': self.get_music_src(id),
                'lyric': self.get_lyric(id),
                'img_src': self.get_background(info.get('name')),
                'info': list_name,
                'play_list': play_music_page[0],
                'similar_music': play_music_page[1]
            }
            return render(request, 'music.html', self.add_username(request, dict))
        except:
            return render(request, 'template.html', self.add_username(request, {}))

    def post(self, request):
        return search(request)

class play_list(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        categogy = request.GET.get('cat')
        info = self.get_play_list(categogy)
        dict = {}
        dict['play_list'] = info[0]
        dict['category'] = info[1]
        return render(request, 'play_list.html', self.add_username(request, dict))

    def post(self, request):
        return search(request)


class album(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        id = request.GET.get('id')
        info = self.album_detail(id)
        dict = {}
        dict['info'] = info[0]
        dict['user'] = info[1]
        dict['album'] = info[2]
        dict['music'] = info[3]
        return render(request, 'album.html', self.add_username(request, dict))

    def post(self, request):
        return search(request)

class music_list(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        id = request.GET.get('id')
        try:
            info = self.playlist_detail(id)
            dict = {
                'info': info[0],
                'music_list': info[1],
                'hot_playlist': info[2],
                'user': info[3]
            }
        except:
            return render(request, 'template.html')
        return render(request, 'music_list.html', self.add_username(request, dict))

    def post(self, request):
        return search(request)

class artist(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        id = request.GET.get('id')
        category = request.GET.get('cat')
        info = self.artist_detail(id, category)
        dict = {
            'info': info[0],
            'detail': info[1],
            'cat': category
        }
        return render(request, 'artist.html', self.add_username(request, dict))

    def post(self, request):
        return search(request)

class top_list(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        id = request.GET.get('id')
        info = self.top_list_detail(id)
        dict = {
            'info': info[0][0],
            'top_lists_charac': info[1],
            'top_lists_global': info[2],
            'songs': info[3]
        }
        return render(request, 'top_list.html', self.add_username(request, dict))

    def post(self, request):
        return search(request)

class dj(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        id = request.GET.get('id')
        return HttpResponseRedirect('/ac/music/?id={}'.format(self.dj_detail(id)[0].get('music_id')))

    def post(self, request):
        return search(request)

class user(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        id = request.GET.get('id')
        info = self.user_detail(id)
        dict = {
            'info': info[0],
            'create': info[1],
            'collec': info[2]
        }
        return render(request, 'user.html', self.add_username(request, dict))

    def post(self, request):
        return search(request)

class mv(View, Yun_Music):

    def get(self, request):
        Yun_Music.__init__(self)
        dict = {
            'lala': 'http://v4.music.126.net/20180427183740/9eb6d8fbc42eef1f4ac5b9c0b8b67ac6/web/cloudmusic/mv/20171225021126/5eab069b-9681-44e0-8db4-3cbcd2d87d6d/c251f005d2fcc28b8c5013ece7a70a93.mp4',
        }
        return render(request, 'mv.html', self.add_username(request, dict))

    def post(self, request):
        return search(request)

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
        if request.POST.get('login'):
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
                return render(request, 'login.html', self.add_username(request, self.dict))
        else:
            return search(request)