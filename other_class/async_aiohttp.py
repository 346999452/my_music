#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: async_aiohttp
    @date: 2018/07/13
    
"""
import asyncio, aiohttp, time, re, async_timeout, json
from random import choice
from other_class.methods import Methods

class Async_Http():
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
        self.header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Requested-With": "xmlHttpRequest",
            'Connection': 'keep-alive',
            "User-Agent": choice(self.user_agent_list),
            "Referer": "https://music.163.com",
            "Accept": "*/*",
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        }
        self.users = ['29879272', '100167517', '58426904', '93504818', '46998208',
                 '278438485', '91239965', '324314596', '1611157', '2313954', '630423930']
        self.path = Methods.absolute_path

    '''
        获取网页内容
    '''
    async def fetch(self, session, url):
        async with async_timeout.timeout(10):
            async with session.get(url, headers = self.header) as response:
                return await response.text()

    async def request(self, url):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, url)

    async def save_info(self, user):
        content = await self.request('http://music.163.com/user/home?id=' + user)
        data = await self.request('http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=' + user)
        data = json.loads(data)['playlist']

        return_list = []

        dict_re = {
            'fans': r'fan_count">(\d+)',
            'event': r'event_count">(\d+)',
            'follow_count': r'follow_count">(\d+)',
            'des': r'inf s-fc3 f-brk">个人介绍：([^<]+)',
            'city': r'(所在地区：[^<]+)',
            'info': r'title": "([^"]+)",\n"images": \["([^"]+)',
            'artist': r'/artist\?id=(\d+)'
        }

        def find(name):
            return re.findall(re.compile(dict_re[name]), content)[0]

        def get_info(name):
            try:
                info = find(name)
            except:
                info = '无'
            return info

        info = get_info('info')
        try:
            artist = find('artist')
            is_artist = True
        except:
            artist = ''
            is_artist = False
        return_list.append({
            'fans': find('fans'),
            'event': find('event'),
            'follow_count': find('follow_count'),
            'img': info[1],
            'name': info[0],
            'des': get_info('des'),
            'city': get_info('city'),
            'artist': artist,
            'is_artist': is_artist
        })

        playlist = [{
            'ordered': i['ordered'],
            'img': i['coverImgUrl'],
            'id': i['id'],
            'name': i['name']
        } for i in data]

        return_list.append(list(filter(lambda x: not x['ordered'], playlist)))
        return_list.append(list(filter(lambda x: x['ordered'], playlist)))
        with open(self.path + 'json/user_' + user + '.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(return_list))
        return return_list

    def asy(self):
        task = [asyncio.ensure_future(self.save_info(user)) for user in self.users]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task))
        return task

    '''
        多url异步爬取入口
        @urls: url列表
    '''
    def main(self, urls):
        task = [asyncio.ensure_future(self.request(url)) for url in urls]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task))
        return task

if __name__ == '__main__':
    start = time.time()
    ah = Async_Http()
    task = ah.asy()
    for i in task:
        print(i.result())
    end = time.time()
    print(end - start)