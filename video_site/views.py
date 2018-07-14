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
from django.forms.models import model_to_dict

# Create your views here.

add_username = Methods.add_username
get_info = Methods.get_login_info
change = Methods.select

class home(View):
    def get(self, request):
        return render(request, 'home.html', add_username(request,{}))

    def post(self, request):
        category = request.POST.get('category')
        if category:
            dict = {'category': category}
        else:
            dict = {}
        return HttpResponse(json.dumps(change(movie_model, 0, 9, **dict)))

class play(View):

    def get(self, request):
        id = request.GET.get('id')
        return render(request, 'video.html', add_username(request, {
            'id': id,
            'barrage': [model_to_dict(i) for i in barrage.objects.filter(movie_id=id)],
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
            lik = likes.objects.filter(movie_id=movie_id, user_id=user_id)
            for i in user_comment.objects.filter(movie_id=movie_id)[:: -1]:
                try:
                    lik.get(comment_time=i.comment_time, comment_user_id=i.user_id)
                    liked = True
                except:
                    liked = False
                comments_list.append({
                    'username': i.username,
                    'user_id': i.user_id,
                    'comment': i.comment,
                    'likes': i.likes,
                    'comment_time': i.comment_time,
                    'could_delete': True if i.user_id == user_id else False,
                    'liked': liked
                })
            return HttpResponse(json.dumps(comments_list))

class danmu(View):
    def get(self, request):
        movie_id = request.GET.get('movie_id')
        data = []
        for i in barrage.objects.filter(movie_id=movie_id):
            data.append(model_to_dict(i))
        return HttpResponse(json.dumps(data))

    def post(self, request):
        try:
            barrage_form(request.POST).save()
        except:
            pass
        return HttpResponse('弹幕发送成功')

def like(request):
    data = request.POST
    user_id = data.get('user_id')
    if not user_id or user_id == 'None':
        return HttpResponse('请登陆后点赞')
    id = data.get('movie_id')
    comment_user_id = data.get('comment_user_id')
    comment_time = data.get('comment_time')
    likes_form(request.POST).save()
    comment = user_comment.objects.get(
        movie_id=id,
        user_id=comment_user_id,
        comment_time=comment_time)
    comment.likes = comment.likes + 1
    comment.save()
    return HttpResponse('点赞成功')

def unlike(request):
    data = request.POST
    id = data.get('movie_id')
    user_id = data.get('user_id')
    if not user_id or user_id == 'None':
        return HttpResponse('请登陆后取消点赞')
    comment_user_id = data.get('comment_user_id')
    comment_time = data.get('comment_time')

    comment = user_comment.objects.get(
        movie_id=id,
        user_id=comment_user_id,
        comment_time=comment_time)
    comment.likes = comment.likes - 1
    comment.save()
    likes.objects.filter(
        movie_id=id,
        comment_user_id=comment_user_id,
        comment_time=comment_time,
        user_id=data.get('user_id')
    ).delete()
    return HttpResponse('已取消点赞')

def delete(request):
    data = request.POST
    comment_time = data.get('comment_time')
    movie_id = data.get('movie_id')
    user_id = data.get('user_id')
    user_comment.objects.filter(
        movie_id=movie_id,
        user_id=user_id,
        comment_time=comment_time
    ).delete()
    likes.objects.filter(
        movie_id=movie_id,
        comment_user_id=user_id,
        comment_time=comment_time
    ).delete()
    return HttpResponse('已删除该评论')

class search(View):

    def get(self, request):
        keyword = request.GET.get('key')
        try:
            movies = set(movie_model.objects.filter(Q(title__contains=keyword) | Q(slogan__contains=keyword)))
        except:
            movies = None
        return render(request, 'search.html', {
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
        return render(request, 'old_home.html', add_username(request, dict))

    def post(self, request):
        return HttpResponseRedirect('/search/?key=' + request.POST.get('key_word'))

def cat(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/search/?key=' + request.POST.get('key_word'))
    cat = request.GET.get('cat')
    movies = movie_model.objects.filter(category=cat)
    return render(request, 'search.html', {
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