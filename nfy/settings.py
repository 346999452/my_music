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
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

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
SPIDER_MIDDLEWARES = {
   'nfy.middlewares.NfySpiderMiddleware': 543,
}

''' 
   包含在项目中启用的下载器中间件及其顺序的字典
   See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
'''
DOWNLOADER_MIDDLEWARES = {
   'nfy.middlewares.RandomUserAgentMiddleware': 560,
   'nfy.middlewares.ProxyMiddleware': 125,
   'nfy.middlewares.CookiesMiddleware': 126,
}

'''
    以下是scrapy本身提供的下载器中间件，用户不能直接修改
    若要添加自定义的中间件或是禁用中间件需要在以上DOWNLOADER_MIDDLEWARES中设置
'''
# DOWNLOADER_MIDDLEWARES_BASE = {
#     'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
#     'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
#     'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
#     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
#     'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
#     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
#     'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
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

MYSQL_DATABASE = {
    'HOST': 'localhost',
    'USER': 'root',
    'PASSWORD': '921002191',
    'DB': 'my_music',
    'PORT': 3306,
    'CHARSET': 'utf8'
}

USER_AGENT_POOL = [
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
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]

IPPOOL=[
    '116.213.98.6:8080'
]

COOKIEPOOL = [
    {
        'jhad': 'mba_muid=1529378793040105972144; mobilev=html5; shshshfp=9fea734073f9e8021ceb3c677bb61b5b; shshshfpa=62c19140-3620-bb85-6b2f-441f15c679f4-1529378811; shshshfpb=1ea57e33a72d74a3d9b9e59f329c93741ee12b233e3f2f72b5b2877fce; __jda=122270672.1529378793040105972144.1529378793.1529386871.1529466434.3; __jdv=122270672|iosapp|t_335139774|appshare|Qqfriends|1529466434842; __jdc=122270672; sid=14791d1e05175f002b31d88e7bfde760; shshshsID=7623ba5094ae1f4c83fd905fc8f6759a_4_1529466490979; TrackerID=M3VygQSSpAM7bOhY4CEGWFOH4L2ODvVSqRHbu3uiNNvKLUb4AQSDV8Mf83-q7aFtop0dsyTGP5yDXiHL2AGT-9toU3R2k5t2x9Lfe9uSFlQ; pt_key=AAFbKc7sADB4g76Y_KtIOeAzDE3xDUFgSb1sRqW3IDb3WG7vONMFDleBNP7aJWVmlhrb1veKz7I; pt_pin=%E9%99%88%E9%9C%B2%E9%9C%B22001; pt_token=tzteqx7m; pwdt_id=%E9%99%88%E9%9C%B2%E9%9C%B22001; __jdb=122270672.4.1529378793040105972144|3.1529466434; mba_sid=15294664348459038873447501344.4'
    },
]