#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: KAI
    @date: 2018/06/19
    
"""

import requests
from time import time
import random, json, re

shouji = {
    '美图': 10002277,
    'vivo': 10002261,
    'oppo': 10002310,
    '金立': 10002280,
    '华为': 10002275,
    'agm': 10002294,
    '国美': 10002293,
    '努比亚': 10002279,
    '黑莓': 10002288,
    '诺基亚': 10002278,
    '锤子': 10002284,
    '小米': 10002282,
    'SONY': 10002286,
    '360': 10002290,
    '荣耀': 10002316,
    '1+': 10002291,
    '联想': 10002295,
    '糖果': 10002289,
    '海信': 10002296,
    '魅族': 10002274,
    '三星': 10002287
}

url_2 = 'https://sign.jd.com/score/sysScore?activityId=10002294&sourceName=sz_tongtianta_1&score=500&gameId=15&_={}&callback=jsonp{}'.format(int(time() * 1000), random.randrange(4, 50))

header = {
    "Host": "sign.jd.com",
    "Referer":"https://h5.m.jd.com/dev/CHNK4jEuwUa3XAaxnTTV8s85XXE/index.html?gameId=15&activityId=10002286&activityKey=05272d959c61498fb5af2c3ddd28f38d&sid=80337318ec270dfc3f244fba408b07dc",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; WAS-AL00 Build/HUAWEIWAS-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 V1_AND_SQ_7.6.5_864_YYB_D QQ/7.6.5.3595 NetType/WIFI WebP/0.3.0 Pixel/1080',
    'Cookie': 'mba_muid=1529378793040105972144; mobilev=html5; shshshfp=9fea734073f9e8021ceb3c677bb61b5b; shshshfpa=62c19140-3620-bb85-6b2f-441f15c679f4-1529378811; shshshfpb=1ea57e33a72d74a3d9b9e59f329c93741ee12b233e3f2f72b5b2877fce; __jdv=122270672|iosapp|t_335139774|appshare|Qqfriends|1529466434842; TrackerID=M3VygQSSpAM7bOhY4CEGWFOH4L2ODvVSqRHbu3uiNNvKLUb4AQSDV8Mf83-q7aFtop0dsyTGP5yDXiHL2AGT-9toU3R2k5t2x9Lfe9uSFlQ; pt_key=AAFbKc7sADB4g76Y_KtIOeAzDE3xDUFgSb1sRqW3IDb3WG7vONMFDleBNP7aJWVmlhrb1veKz7I; pt_pin=%E9%99%88%E9%9C%B2%E9%9C%B22001; pt_token=tzteqx7m; pwdt_id=%E9%99%88%E9%9C%B2%E9%9C%B22001; __jda=122270672.1529378793040105972144.1529378793.1529466434.1529504694.4; __jdc=122270672; sid=80337318ec270dfc3f244fba408b07dc; __jdb=122270672.5.1529378793040105972144|4.1529504694; mba_sid=15295046947808538280749254787.5'
}

header_2 = {
    "Host": "sign.jd.com",
    "Referer":"https://h5.m.jd.com/dev/CHNK4jEuwUa3XAaxnTTV8s85XXE/index.html?gameId=15&activityId=10002294&activityKey=b4cb06895cc1410fa387a41f8f8f917d",
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/30.0.1599.12 Mobile/11A501 Safari/8536.25 MicroMessenger/6.1.0',
    'Cookie': 'mba_muid=1529378793040105972144; mobilev=html5; shshshfp=9fea734073f9e8021ceb3c677bb61b5b; shshshfpa=62c19140-3620-bb85-6b2f-441f15c679f4-1529378811; shshshfpb=1ea57e33a72d74a3d9b9e59f329c93741ee12b233e3f2f72b5b2877fce; __jda=122270672.1529378793040105972144.1529378793.1529386871.1529466434.3; __jdv=122270672|iosapp|t_335139774|appshare|Qqfriends|1529466434842; __jdc=122270672; sid=14791d1e05175f002b31d88e7bfde760; shshshsID=7623ba5094ae1f4c83fd905fc8f6759a_4_1529466490979; TrackerID=M3VygQSSpAM7bOhY4CEGWFOH4L2ODvVSqRHbu3uiNNvKLUb4AQSDV8Mf83-q7aFtop0dsyTGP5yDXiHL2AGT-9toU3R2k5t2x9Lfe9uSFlQ; pt_key=AAFbKc7sADB4g76Y_KtIOeAzDE3xDUFgSb1sRqW3IDb3WG7vONMFDleBNP7aJWVmlhrb1veKz7I; pt_pin=%E9%99%88%E9%9C%B2%E9%9C%B22001; pt_token=tzteqx7m; pwdt_id=%E9%99%88%E9%9C%B2%E9%9C%B22001; __jdb=122270672.4.1529378793040105972144|3.1529466434; mba_sid=15294664348459038873447501344.4'
}

url_3 = 'http://39.106.179.219/ac/lala'
url_4 = 'http://music.163.com/discover/playlist/'

proxy = {
    # 'http': 'http://221.232.195.14:808',
}

def get_score(pai, header):
    sc_url = 'https://sign.jd.com/score/queryRankingList?activityId={}&sourceName=sz_tongtianta_1&type=4&startRankNo=0&endRankNo=199&_={}&callback=jsonp{}'.format(shouji.get(pai), int(time() * 1000), random.randrange(4, 50))
    info = requests.get(url=sc_url, headers=header).content.decode('utf-8')
    dic = json.loads(re.findall(re.compile(r'[^{]+([^\)]+)'), info)[0])
    return dic.get('model')

def tijiao(pai, score, header):
    tj_url = 'https://sign.jd.com/score/sysScore?activityId={}&sourceName=sz_tongtianta_1&score={}&gameId=15&_={}&callback=jsonp{}'.format(shouji.get(pai), score, int((time() - 3600 * 24 * 13)  * 1000), random.randrange(4, 50))
    info = requests.get(url=tj_url, headers=header).content.decode('utf-8')
    return info



if __name__ == '__main__':
    # for i in get_score('华为', header):
    #     print(i)
    # from time import sleep
    #
    # while 1:
    #     print(time())
    #     sleep(1)
    # tijiao('黑莓', '500', header)
    dict = {
        'oe': 0,
        'n': 0,
        'z': 0,
        'oK': 1,
        '6': '1',
        '5': 1,
        'ow': 2,
        '-': 2,
        'A': 2,
        'oi': 3,
        'o': 3,
        'i': 3,
        '7e': 4,
        'v': 4,
        'P': 4,
        '7K': 5,
        '4': 5,
        'k': 5,
        '7w': 6,
        'C': 6,
        's': 6,
        '7i': 7,
        'S': 7,
        'l': 7,
        'Ne': 8,
        'c': 8,
        'F': 8,
        'NK': 9,
        'E': 9,
        'q': 9,
        '*': 'X'
    }
    key = '*S1*7wnioKnAoeCz'
    a = ['6', '0', '3', '1', '0', '2', '0', '6', '0']
    str_2 = '603102060'
    key = key[4:]
    n = 0
    # for i in range(len(key)):
    #     if dict.get(key[n: n + 2]):
    #         key.replace(1, 2)

    # from datetime import datetime
    # print(datetime.now().year)
    # print(1)
    import base64
    print(base64.b64decode('Y29udGFjdEBraW5nbmFtZS5pbmZvCg==').decode('utf-8'))

    '''
        1440081377
        *S1*oKvPoK6kow6 zNK ni7K4Poioq
        
        144 11521 09 03554339
        
        346999452
        *S1*oKvPoK6kow6 5oe CFoKcA7eCP
        144 11521 10 68182464
        
        419483502
        *S1*oKvPoK6kow6 zNK -P7eoPoi-A
        144 11521 09 24434322
    '''