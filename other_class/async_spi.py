#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: async_spi
    @date: 2018/07/06
    
"""

import asyncio
from aiohttp import ClientSession
import time, re

start = time.time()

users = ['29879272', '100167517', '58426904', '93504818', '46998208',
         '278438485', '91239965', '324314596', '1611157', '2313954']

header = {
    "Host": "music.163.com",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; WAS-AL00 Build/HUAWEIWAS-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 V1_AND_SQ_7.6.5_864_YYB_D QQ/7.6.5.3595 NetType/WIFI WebP/0.3.0 Pixel/1080',
}

async def get(url):
    async with ClientSession() as sess:
        response = await sess.get(url, headers=header)
        result = await response.text()
        return result

async def tiqu(url):
    text = await get(url)
    pattern = re.compile(r'navbar-brand">([^<]+)')
    return re.findall(pattern, text)

async def get_user_info(user):
    content = await get('http://music.163.com/user/home?id=' + user)
    # data = await get('http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=' + user)
    # return_list = []
    #
    # dict_re = {
    #     'fans': r'fan_count">(\d+)',
    #     'event': r'event_count">(\d+)',
    #     'follow_count': r'follow_count">(\d+)',
    #     'des': r'inf s-fc3 f-brk">个人介绍：([^<]+)',
    #     'city': r'(所在地区：[^<]+)',
    #     'info': r'title": "([^"]+)",\n"images": \["([^"]+)',
    #     'artist': r'/artist\?id=(\d+)'
    # }
    #
    # def find(name):
    #     return re.findall(dict_re[name], content)[0]
    #
    # def get_info(name):
    #     try:
    #         info = find(name)
    #     except:
    #         info = '无'
    #     return info
    #
    # info = get_info('info')
    # try:
    #     artist = find('artist')
    #     is_artist = True
    # except:
    #     artist = ''
    #     is_artist = False
    # return_list.append({
    #     'fans': find('fans'),
    #     'event': find('event'),
    #     'follow_count': find('follow_count'),
    #     'img': info[1],
    #     'name': info[0],
    #     'des': get_info('des'),
    #     'city': get_info('city'),
    #     'artist': artist,
    #     'is_artist': is_artist
    # })
    #
    # playlist = [{
    #     'ordered': i['ordered'],
    #     'img': i['coverImgUrl'],
    #     'id': i['id'],
    #     'name': i['name']
    # } for i in data]
    #
    # return_list.append(list(filter(lambda x: not x['ordered'], playlist)))
    # return_list.append(list(filter(lambda x: x['ordered'], playlist)))

    return content

async def request(user):
    result = await get_user_info(user)
    return result

def callback(task):
    print('Status', task.result())

task = [asyncio.ensure_future(request(user)) for user in users]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task))

for t in task:
    print('Task Result:', t.result())

end = time.time()
print('Cost time:', end - start)

