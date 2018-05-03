#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: http_client
    @date: 2018/01/24
    
"""
import json, requests
from random import choice

'''
    一些应用的API
    https://github.com/jokermonn/-Api
'''

class Http_Client():

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    ]

    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers.update(self.set_header())

    ''' 设置cookies '''
    def set_cookies(self, **kwargs):
        for k, v in kwargs.items():
            self.sess.cookies.set(k, v)

    ''' 删除所有的key '''
    def del_cookies(self):
        self.sess.cookies.clear()

    ''' 删除指定key的session '''
    def del_cookies_by_key(self, key):
        self.sess.cookies.set(key, None)

    ''' 设置header '''
    def set_header(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Requested-With": "xmlHttpRequest",
            'Connection': 'keep-alive',
            "User-Agent": choice(self.user_agent_list),
            "Referer": "http://39.106.179.219:8000/",
            "Accept": "*/*",
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        }

    def set_headers(self, headers):
        self.sess.headers.update(headers)
        return self

    def reset_headers(self):
        self.sess.headers.clear()
        self.sess.headers.update(self.set_header())

    def set_headers_referer(self, referer):
        self.sess.headers.update({"Referer": referer})
        return self

    def send(self, url, data=None, **kwargs):
        error_data = {"code": 99999, "data": ""}
        self.set_headers_referer(url.split('//')[0] + '//' + url.split('//')[1].split('/')[0])
        if data:
            method = "post"
            self.set_headers({"Content-Length": "{0}".format(len(data))})
        else:
            method = "get"
            self.reset_headers()
        try:
            response = self.sess.request(method=method, timeout=10, url=url, data=data, **kwargs)
            if response.content:
                try:
                    str = response.content.decode('utf-8')
                except:
                    str = response.content
                return json.loads(str) if method == "post" else str
            else:
                return error_data
        except:
            return error_data