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

    ''' 
        设置header 
        
        content-type:
            指定提交数据的形式
                
            application/x-www-form-urlencoded：表单数据
            application/json：序列化json数据
            multipart/form-data：表单文件上传
            text/xml：xml数据
    '''
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

    '''
        常见代码及详情：
            代码              说明              详情   
            
            100              继续             请求者应当继续提出请求。服务器已收到请求的一部分，正在等待剩余部分
            101              切换协议         请求者已要求服务器切换协议，服务器已确认并准备切换
            200              成功             服务器已成功处理请求
            201              已创建           请求成功并且服务器创建了新的资源 
            202              已接受            服务器已接受请求，但并未处理
            203             非授权信息         服务器已处理请求，但返回的信息可能来自另一个源
            204              无内容            服务器成功处理了请求，但没有返回任何内容  
            205              重置内容         服务器成功处理了请求，内容被重置
            206             部分内容           服务器成功处理了部分请求
            300             多种选择          针对请求，服务器可执行多种操作
            301             永久移动           请求的网页已永久移动到新位置，即永久重定向
            302             临时移动           请求的网页暂时跳转到其他页面
            303            查看其他位置        如果原来的请求是POST，重定向目标文档应该通过GET提取
            304              未修改            此次请求返回的网页未修改，继续使用上次的资源
            305             使用代理           请求这应该使用代理访问该网页
            307             临时重定向         请求的资源临时从其他位置响应
            400             错误请求           服务器无法解析该请求
            401              未授权            请求没有进行身份验证或验证未通过
            403             禁止访问           服务器拒绝此请求
            404              未找到            服务器找不到请求的网页
            405             方法禁用           服务器禁用了请求中指定的方法
            406              不接受            无法使用请求的内容响应请求的网页
            407            需要代理授权        请求者需要使用代理授权
            408             请求超时           服务器请求超时
            409               冲突             服务器在完成请求时发生冲突
            410              已删除            请求的资源已永久删除
            411            需要有效长度        服务器不接受不含有效内容长度标头字段的请求
            412           未满足前提条件        服务器为满足请求者在请求中设置的其中一个前提条件
            413            请求实体过大        请求实体过大，超出服务器处理能力
            414            请求url过长         请求网址过长，服务器无法处理
            415            不支持类型           请求格式不被请求页面支持
            416            请求范围不符        页面无法提供请求的范围
            417            未满足期望值         服务器未满足期望请求标头字段的要求
            500           服务器内部错误        服务器遇到错误，无法完成请求
            501               未实现           服务器不具备完成请求的功能
            502              错误网关          服务器作为网关或代理，从上游服务器收到无效响应
            503             服务不可用          服务器目前无法使用
            504              网关超时           服务器作为网关或代理，但是没有及时从上游服务器收到请求
            505           HTTP版本不支持        服务器不支持请求中所用的HTTP协议版本     
                    
    '''
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