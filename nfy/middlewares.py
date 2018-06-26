# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: __init__
    @time: 2018/05/06

    中间件
    see http://doc.scrapy.org/en/latest/topics/spider-middleware.html

    Downloader Middleware:
        下载器中间件，位于引擎和下载器之间的钩子框架，主要处理引擎和下载器之间的请求和响应
        核心方法（实现其中一个方法就可以定义一个Downloader Middleware）：
            process_request(request, spider)
            process_response(request, response, spider)
            precess_exception(request, exception, spider)

    Spider Middleware:
        蜘蛛中间件，位于引擎和蜘蛛之间的钩子框架，主要处理蜘蛛输入的响应和输出结果及新的请求
        核心方法（实现其中一个方法就可以定义一个Spider Middleware）：
            process_spider_input(response, spider)
            process_spider_output(response, result, spider)
            process_spider_exception(response, exception, spider)
            process_start_requests(start_requests, spider)
"""

from scrapy import signals
import random

class NfySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    '''
        这个方法在将response发往spider的过程中被调用
        这个方法应该返回一个None或raise一个异常
        response：正在响应的处理
    '''
    def process_spider_input(self, response, spider):
        return None

    '''
        这个方法将在request或者item法网engine的过程中被调用
        这个方法必须返回一个response，dict，item
        result：（一个request，dict，item）有这个spider返回的结果
    '''
    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    '''
        这个方法在一个spider或者一个process_spider_input方法抛出异常的时候被调用
        应该返回None或者一个response，dict，item
    '''
    def process_spider_exception(self, response, exception, spider):
        pass

    '''
        用来处理发往engine的请求，和process_spider_output唯一不同的地方是，不接受response，
        并且只能返回一个request
    '''
    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware():

    def __init__(self, user_agents):
        self.user_agents = user_agents

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agents=crawler.settings.get('USER_AGENT_POOL'))

import requests, json

class CookiesMiddleware():

    def __init__(self, cookies_url):
        self.cookies_url = cookies_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        # self.logger.debug('正在获取Cookies')
        # cookies = self.get_random_cookies()
        # if cookies:
        if spider.name == 'exam':
            request.cookies = random.choice(self.cookies_url)
            # self.logger.debug('使用Cookies ' + json.dumps(cookies))

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(cookies_url=settings.get('COOKIEPOOL'))

class ProxyMiddleware():

    def __init__(self, proxy_urls):
        self.proxy_urls = proxy_urls

    def process_request(self, request, spider):
        pass
        # request.meta['proxy'] = 'http://{}'.format(random.choice(self.proxy_urls))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(proxy_urls=crawler.settings.get('IPPOOL'))

'''
    对接selenium
'''
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from scrapy.http import HtmlResponse

# class SeleniumMiddleware():
#     def __init__(self, timeout=None):
#         self.browser = webdriver.PhantomJS()
#
#     def __del__(self):
#         self.browser.close()
#
#     def process_request(self, request, spider):
#         if spider.name == 'selenium':
#             pass
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         settings = crawler.settings
#         return cls(
#             timeout=settings.get('SELENIUM_TIMEOUT')
#         )