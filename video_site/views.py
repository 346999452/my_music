#! usr/bin/env python
# -*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: view
    @date: 2018/07/03

"""

from django.shortcuts import render
from django.views import View
from music_site.forms import *
from django.http import HttpResponseRedirect, HttpResponse
import time, json
from django.db.models import Q
from other_class.methods import Methods

# Create your views here.

add_username = Methods.add_username
get_info = Methods.get_login_info

def shi(request):
    return render(request, 'shi.html', add_username(request, {}))

class play(View):

    def get(self, request):
        id = request.GET.get('id')
        return render(request, 'video.html', add_username(request, {
            'id': id,
            'url': movie_model.objects.get(id=id).play_url,
        }))

    def post(self, request):
        username, user_id = get_info(request)
        data = request.POST
        if data.get('user_comment'):
            comment_time = time.strftime('%Y/%m/%d | %H:%M:%S', time.localtime())
            try:
                user_comment(
                    movie_id=data.get('movie_id'),
                    user_id=user_id,
                    comment=data.get('user_comment'),
                    comment_time=comment_time,
                    username=username
                ).save()
            except:
                return HttpResponse('请登陆后评论')
            return HttpResponse('评论成功')
        else:
            comments_list = []
            movie_id = data.get('movie_id')

            lik = likes.objects.filter(Q(movie_id=movie_id) | Q(user_id=user_id))
            for i in user_comment.objects.filter(movie_id=movie_id):
                comments_list.append({
                    'username': i.username,
                    'user_id': i.user_id,
                    'comment': i.comment,
                    'likes': i.likes,
                    'comment_time': i.comment_time,
                    'could_delete': True,
                    'liked': True
                })
            return HttpResponse(json.dumps(comments_list))



def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('username')
    response.delete_cookie('loginname')
    return response

def cat(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/search/?key=' + request.POST.get('key_word'))
    cat = request.GET.get('cat')
    movies = movie_model.objects.filter(category=cat)
    return render(request, 'js/search.html', {
        'cat': cat,
        'info': movies,
        'part': [{
            'href': '#portfolio',
            'title': '查询结果'
        }, {
            'href': '#packages',
            'title': '分类'
        }, {
            'href': '#contactUs',
            'title': '搜索'
        }]
    })

def like(request):
    like = likes_form(request.GET)
    loginname = request.GET.get('loginname')
    if not loginname or loginname == 'None':
        return HttpResponseRedirect('/login')
    id = request.GET.get('movie_id')
    comment_username = request.GET.get('comment_username')
    comment_time = request.GET.get('comment_time')
    comment = user_comment.objects.get(
        movie_id=id,
        comment_username=comment_username,
        comment_time=comment_time)
    comment.likes = comment.likes + 1
    comment.save()
    like.save()
    return HttpResponseRedirect('/image/?id={}'.format(id))

def unlike(request):
    loginname = request.GET.get('loginname')
    id = request.GET.get('movie_id')
    comment_username = request.GET.get('comment_username')
    comment_time = request.GET.get('comment_time')
    comment = user_comment.objects.get(
        movie_id=id,
        comment_username=comment_username,
        comment_time=comment_time)
    comment.likes = comment.likes - 1
    comment.save()
    likes.objects.filter(
        movie_id=id,
        comment_username=comment_username,
        comment_time=comment_time,
        loginname=loginname
    ).delete()
    return HttpResponseRedirect('/image/?id={}'.format(id))

def shanchu(request):
    id = request.GET.get('movie_id')
    comment_username = request.GET.get('comment_username')
    comment_time = request.GET.get('comment_time')
    comment = user_comment.objects.filter(
        movie_id=id,
        comment_username=comment_username,
        comment_time=comment_time
    ).delete()
    return HttpResponseRedirect('/image/?id={}'.format(id))

class search(View):

    def get(self, request):
        keyword = request.GET.get('key')
        try:
            movies = set(movie_model.objects.filter(Q(title__contains=keyword) | Q(slogan__contains=keyword)))
        except:
            movies = None
        return render(request, 'js/search.html', {
            'info': movies,
            'key_word': keyword,
            'part': [{
                'href': '#portfolio',
                'title': '查询结果'
            }, {
                'href': '#packages',
                'title': '分类'
            }, {
                'href': '#contactUs',
                'title': '搜索'
            }]
        })

    def post(self, request):
        return HttpResponseRedirect('/search/?key=' + request.POST.get('key_word'))

class index(View):

    def get(self, request):
        dict = {
            'info': movie_model.objects.all()[: 9],
            'part': [{
                'href': '#portfolio',
                'title': '推荐'
            }, {
                'href': '#packages',
                'title': '分类'
            }, {
                'href': '#contactUs',
                'title': '搜索'
            }]
        }
        return render(request, 'home.html', add_username(request, dict))

    def post(self, request):
        return HttpResponseRedirect('/search/?key=' + request.POST.get('key_word'))

class play_video(View):

    def get(self, request):
        username = get_username(request)
        id = request.GET.get('id')
        if id:
            request.session['id'] = id
        else:
            id = request.session.get('id')
        info = movie_model.objects.get(id=id)
        comments_list = []
        for i in user_comment.objects.filter(movie_id=id):
            try:
                likes.objects.get(
                    comment_username=i.comment_username,
                    comment_time = i.comment_time,
                    loginname = request.COOKIES.get('loginname', None)
                )
                liked = True
            except:
                liked = False
            if i.comment_username == username:
                p = True
            else:
                p = False
            comments_list.append({
                'comment_username': i.comment_username,
                'comment_time': i.comment_time,
                'user_comment': i.user_comment,
                'liked': liked,
                'likes': i.likes,
                'p': p
            })
        dict = {
            'id': id,
            'url': info.play_url,
            'comments_list': comments_list,
            'username': username,
            'loginname': request.COOKIES.get('loginname', None),
            'part': [{
                'href': '#image',
                'title': '视频'
            }, {
                'href': '#danmu',
                'title': '弹幕'
            }, {
                'href': '#comment',
                'title': '评论'
            }]
        }
        return render(request, 'js/play.html', add_username(request, dict))

    def post(self, request):
        comment_time = time.strftime('%Y/%m/%d | %H:%M:%S', time.localtime())
        try:
            user_comment(
                movie_id = request.session.get('id'),
                comment_username = get_username(request),
                user_comment = request.POST.get('user_comment'),
                comment_time = comment_time).save()
        except:
            return HttpResponseRedirect('/login')
        return HttpResponseRedirect(request.path)