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

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
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

import logging, requests, json

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