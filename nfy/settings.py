# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: settings
    @time: 2018/05/06

    项目设置模块

    可以从下列网址中获取更多配置信息
       http://doc.scrapy.org/en/latest/topics/settings.html
       http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
       http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

"""

import os

''' Scrapy项目名称 '''
BOT_NAME = 'nfy'

SPIDER_MODULES = ['nfy.spiders']

''' 模块在哪里使用genspider命令创建新的爬虫， 默认为'' '''
NEWSPIDER_MODULE = 'nfy.spiders'

''' 检索时使用的默认用户代理，默认为'Scrapy/VERSION (+http://scrapy.org)' '''
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

''' 是否遵守机器人协议 '''
ROBOTSTXT_OBEY = True

''' scrapy下载程序执行的并发请求的最大数量， 不设置时默认为16 '''
CONCURRENT_REQUESTS = 32

''' 
   下载器在从同一网站下载连续页面之前应等待的时间（以秒为单位）
   这可以用于限制爬取速度，以避免被服务器限制。支持小数， 默认为0
   See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
'''
DOWNLOAD_DELAY = 0.25

''' 
   对任何单个域执行的并发请求最大数量，默认为8 
   与CONCURRENT_REQUESTS_PER_IP间只会实现一个
'''
CONCURRENT_REQUESTS_PER_DOMAIN = 16

''' 
   对任何单个IP执行的并发请求最大数量， 默认为0
   如果非0，则忽略CONCURRENT_REQUESTS_PER_DOMAIN配置，改为使用此设置
   此设置也会影响DOWNLOAD_DELAY和AutoThrottle扩展
'''
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

''' 指定是否启用telnet控制台，默认为True '''
#TELNETCONSOLE_ENABLED = False

''' 用于Scrapy Http请求的默认标头 '''
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
  'Accept-Encoding': 'gzip, deflate, sdch',
  'Connection': 'keep-alive'
}

''' 
   包含在项目中启用的爬虫中间件的字典及其顺序
   See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
'''
# SPIDER_MIDDLEWARES = {
#    'nfy.middlewares.NfySpiderMiddleware': 543,
# }

''' 
   包含在项目中启用的下载器中间件及其顺序的字典
   See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
'''
# DOWNLOADER_MIDDLEWARES = {
#    'nfy.middlewares.MyCustomDownloaderMiddleware': 543,
# }

'''
   包含项目中启用的扩展名及其顺序的字典
   See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
'''
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
}

''' 
   包含要使用的项目管道及其顺序的字典。
   顺序值是任意的，但通常将他们定义在0-1000范围内，先处理较低顺序值的
   See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
'''
ITEM_PIPELINES = {
   'nfy.pipelines.NfyPipeline': 300,
}

'''
   是否启用自动限速扩展，默认为False
   See http://wiki.jikexueyuan.com/project/scrapy/autothrottle.html
'''
#AUTOTHROTTLE_ENABLED = True

''' 自动限速初始下载延迟，单位秒，默认为5 '''
#AUTOTHROTTLE_START_DELAY = 5

''' 在高延迟情况下最大的下载延迟，单位秒，默认60 '''
#AUTOTHROTTLE_MAX_DELAY = 60

# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

''' 
   启用AutoThrottle调试模式，展示每个接收到的response 
   可以通过此来查看限速参数是如何实时被调整的
   默认为False
'''
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

''' 项目路径 '''
PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.curdir))

''' 异步任务队列 '''
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

''' 广度优先 '''
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
