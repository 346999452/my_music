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

def home(request):
    ym = Yun_Music()
    info = ym.get_index()

    dict = {'new_song_list': ym.get_top_10(),
            'up_song_list': ym.get_top_10('云音乐飙升榜'),
            'original_song_list': ym.get_top_10('网易原创歌曲榜'),
            'hot_song_list': ym.get_top_10('云音乐热歌榜'),
            'singer_list': info[3],
            'popular_anchor': info[4],
            'play_list': info[5],
            'album_list': info[7],
            'img': 'http://p1.music.126.net/EBUS_i_M8M8xKMW0dSOfPg==/109951163236930035.jpg'
        }
    return render(request, 'index.html', Methods.add_username(request, dict))

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

class register(View):
    dict = {}

    def get(self, request):
        return render(request, 'register.html', Methods.add_username(request, self.dict))

    def post(self, request):
        usr = user_form(request.POST)
        if usr.is_valid():
            img = request.POST.get('face')
            loginname = Methods.hash(usr.cleaned_data['loginname'])
            try:
                user.objects.get(loginname=loginname)
                self.dict['user_exit'] = True
                return render(request, 'register.html', Methods.add_username(request, self.dict))
            except:
                face_url = Methods.get_str()
                user(
                    username=usr.cleaned_data['username'],
                    loginname=loginname,
                    password=Methods.hash(usr.cleaned_data['password']),
                    face=face_url
                ).save()
                return HttpResponseRedirect('/ac/login')
        else:
            self.dict['str_error'] = True
            return render(request, 'register.html', Methods.add_username(request, self.dict))

class login(View):
    dict = {'title': '登录', 'year': datetime.now().year, }

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