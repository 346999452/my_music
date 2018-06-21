# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: yun_music
    @time: 2018/04/05
    
"""
from other_class.http_client import Http_Client
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from other_class.methods import Methods
import base64, json, re
from urllib.request import quote
from bs4 import BeautifulSoup
from random import choice

class Yun_Music(Methods, Http_Client):

    def __init__(self):
        Http_Client.__init__(self)
        self.set_header()
        self.top_list_urls = self.get_json('json/top_list.json')

        ''' 映射字典的key值(共用) '''
        self.list_name = [
            ['id', 'name', 'rank'],
            ['singer', 'identity', 'img', 'id'],
            ['img', 'url'],
            ['id', 'name', 'artist', 'artist_id', 'img'],
        ]

    secKey = '1234567890ABCDEF'

    ''' 歌曲id加密 '''
    def get_params(self, dict):
        text = json.dumps(dict)
        nonce = '0CoJUm6Qyw8W8jud'
        params = self.aes(self.aes(text, nonce).decode("utf-8"), self.secKey)
        return params

    '''
        每个secKey和encSecKey一一对应，每次更改secKey时执行下rsa_encrypt方法
        这里为了省时间就固定了secKey和encSecKey
        pubKey = '010001'
        modules = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    def rsa_encrypt(self):
        text = self.secKey[::-1]
        rs = int(self.hex(text), 16) ** int(self.pubKey, 16) % int(self.modules, 16)
        return format(rs, 'x').zfill(256)

    def hex(self, s):
        import codecs
        return codecs.encode(bytes(s, encoding="utf8"), 'hex')
    '''

    ''' aes加密 '''
    def aes(self, text, sec_key):
        backend = default_backend()
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        cipher = Cipher(
            algorithms.AES(sec_key.encode('utf-8')),
            modes.CBC(b'0102030405060708'),
            backend=backend
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(text.encode('utf-8')) + encryptor.finalize()
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    ''' 
        通过id得到音乐的url
        网易云音乐的mp3地址有时会更换，故这里每次都获取下歌曲的地址 
        详细参见：https://github.com/darknessomi/musicbox/wiki/%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90%E6%96%B0%E7%89%88WebAPI%E5%88%86%E6%9E%90%E3%80%82
    '''
    def get_music_src(self, id):
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        data = {
            'params': self.get_params({
                'ids': '[{}]'.format(id),
                'br': '320000',
                'csrf_token': 'csrf'
            }),
            'encSecKey': '08ffac1245c7c48e91872468d5e897d69f8c0671ef97b746c84bad75f22e9a3eca8c292e7c4d67e4df7576a7db511a36112117a013c0ffe2d70fa2f067f6e9db9004bcdd0cfe9abee4eea52736aee39ac8644d46ef7718ebcefe9f1f717848d9f8e528defc438accdd223fafff315b1e96eeae7a4080cad8495f9296243e798c'
        }
        try:
            return self.send(url, data).get('data')[0].get('url')
        except:
            return None

    def login(self, username, password):
        url = 'http://music.163.com/weapi/login/cellphone?csrf_token='
        data = {
            'params': self.get_params({
                'phone': username,
                'password': self.hash(password),
                'rememberLogin': 'true'
            }),
            'encSecKey': '08ffac1245c7c48e91872468d5e897d69f8c0671ef97b746c84bad75f22e9a3eca8c292e7c4d67e4df7576a7db511a36112117a013c0ffe2d70fa2f067f6e9db9004bcdd0cfe9abee4eea52736aee39ac8644d46ef7718ebcefe9f1f717848d9f8e528defc438accdd223fafff315b1e96eeae7a4080cad8495f9296243e798c'
        }
        data = self.send(url, data)
        if 'profile' in data:
            info = data['profile']
            return True, (info['userId'], info['nickname'])
        else:
            if 'msg' in data:
                return False, data['msg']
            else:
                return False, '手机号错误或未注册'

    def logout(self):
        self.send('http://music.163.com/api/logout')

    ''' 得到排行榜信息 '''
    def get_top_list(self, list_name=None):
        if list_name:
            url = 'http://music.163.com' + self.top_list_urls[list_name]
        else:
            url = 'http://music.163.com' + self.top_list_urls['云音乐新歌榜']
        return re.findall(r'/song\?id=(\d+)">([^<]+)', self.send(url))

    ''' 得到榜首音乐的url '''
    def get_top_music(self):
        id = self.get_top_list()[0][0]
        return self.get_music_src(id)

    ''' 获取推荐音乐 '''
    def commend_music(self, list_name=None):
        list_info = []
        rank = 1
        for key, value in self.get_top_list(list_name):
            list_info.append(self.key_value(key, value, rank))
            rank += 1
        return list_info

    def get_list(self):
        list_info = []
        for key, value in self.top_list_urls.items():
            list_info.append(self.key_value(key, value))
        return list_info

    ''' 歌曲详细信息 '''
    def song_detail(self, id):
        url = 'http://music.163.com/api/song/detail/?id={}&ids=[{}]'.format(id, id)
        data = json.loads(self.send(url))
        return data.get('songs')[0]

    ''' 获取各榜单top10详细信息 '''
    def get_top_10(self, list_name=None):
        music_list = self.map_list(self.get_top_list(list_name)[: 10], [i + 1 for i in range(10)], 2)
        song_list = []
        for _ in music_list:
            info = self.song_detail(_[0])
            song_item = {
                'id': _[0],
                'title': _[1],
                'artist': info['artists'][0]['name'],
                'cover_url': info['album']['picUrl'],
                'rank': _[2],
            }
            song_list.append(song_item)
        return song_list

    ''' 得到网易云音乐首页的信息 '''
    def get_index(self):
        content = self.send('http://music.163.com/discover')
        song_list = []

        ''' 爬取首页信息所需正则表达式 '''
        dict_re = {
            'singer_id': r'/user/home\?id=([\d]+)',
            'rank_list': r'/song\?id=(\d+)" class="nm s-fc0 f-thide" title="([^"]+)',
            'singer_img': r'class="j-img" src="([^\?]+\?param=62y62)"',
            'popular_anchor_img': r'data-src="([^\?]+\?param=40y40)"',
            'singer_list': r'class="nm f-fs1 f-ib f-thide">([^<]+)',
            'identity_list': r'class="f-thide s-fc3">([^<]+)',
            'popular_anchor': r'class="nm-icn f-thide s-fc0">([^<]+)',
            'play_list_img': r'src="([^\?]+\?param=140y140)"',
            'play_list': r'title="([^"]+)" href="/([a-z]+)\?id=(\d+)"',
            'lunbo': r'picUrl : "([^"]+)",\nurl : "([^"]+)",',
            'album_list': r'data-src="([^"]+)">\n<a title="([^"]+)" href="/album\?id=(\d+)"',
            'album_list_artist': r'tit f-thide" title="([^"]+)">\n<a class="s-fc3" href="/artist\?id=(\d+)'
        }

        def zip_list(song_list, *args):
            self.add_list(list(zip(*args)), song_list, self.list_name[1])

        def find(name):
            return re.findall(dict_re.get(name), content)

        ''' 首页榜单信息 '''
        for i in range(3):
            self.add_list(list(map(lambda x, y: (x[0], x[1], y), find('rank_list')[i * 10: (i + 1) * 10], [i + 1 for i in range(10)])), song_list, self.list_name[0])

        ''' 爬取网易入驻歌手及热门主播的信息 '''
        zip_list(song_list, find('singer_list'), find('identity_list')[: 5], find('singer_img'), find('singer_id')[: 5])
        zip_list(song_list, find('popular_anchor'), find('identity_list')[5: 10], find('popular_anchor_img'), find('singer_id')[5:: 2])

        ''' 热门推荐的歌单 '''
        self.add_list(list(map(lambda x, y: (x[0], 'music_list' if x[1] == 'playlist' else 'dj',
            '电台节目' if x[1] == 'dj' else '歌单', x[2], y), find('play_list'), find('play_list_img'))), song_list, self.list_name[3])

        def lunbo(lunbo_list):
            li = ['song', 'album', 'mv']
            c = []
            for i in lunbo_list:
                try:
                    id = re.findall(re.compile('id=(\d+)'), i[1])[0]
                    for j in li:
                        if re.search(re.compile(j), i[1]):
                            url = '/ac/{}/?id={}'.format('music' if j == 'song' else j, id)
                            break
                    else:
                        url = i[1]
                except:
                    url = i[1]
                c.append((i[0], url))
            return c

        ''' 轮播图 '''
        self.add_list(lunbo(find('lunbo')), song_list, self.list_name[2])

        ''' 新碟上架 '''
        self.add_list(list(map(lambda x, y: (x[2], x[1], y[0], y[1], x[0]), find('album_list')[: 10], find('album_list_artist')[: 10])), song_list, self.list_name[3])

        return song_list

    ''' 爬取歌单列表信息 '''
    def get_play_list(self, play_list_name=None):
        if play_list_name:
            content = self.send('http://music.163.com/discover/playlist/?cat={}'.format(quote(play_list_name)))
        else:
            content = self.send('http://music.163.com/discover/playlist')
        info = re.findall(r'title="([^"]+)" href="/playlist\?id=(\d+)" class="tit f-thide s-fc0">([^<]+)</a>\n</p>\n<p><span class="s-fc4">by</span> <a title="([^"]+)', content)
        img = re.findall(r'src="([^\?]+\?param=140y140)"', content)
        play_list = []
        category_list = []
        for style in BeautifulSoup(content, 'lxml').find_all('dl'):
            category = [i.strip('|') for i in style.dd.get_text().split('\n') if i is not '']
            category_list.append({'style': style.dt.get_text(), 'name': category})
        self.add_list(list(map(lambda x, y: (x[1], x[0], x[3], y), info, img)), play_list, self.list_name[1])
        play_list.append(category_list)
        return play_list

    ''' 获取音乐歌词 '''
    def get_lyric(self, song_id):
        url = 'http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
        data = json.loads(self.send(url))
        if 'lrc' not in data:
            return ['无歌词']
        lyric_list = []
        for i in (data['lrc']['lyric'] + ('\n' + data['tlyric']['lyric'] if data['tlyric'].get('lyric') else '')).split('\n'):
            if re.findall(r'\[by:([^\]]+)', i):
                name = re.findall(r'\[by:([^\]]+)', i)
                lyric_list.append('翻译：{}'.format(name))
            try:
                lyric_list.append(i.split(']')[1])
            except:
                lyric_list.append(i)
        return lyric_list

    ''' 爬取音乐播放界面信息 '''
    def get_play_music(self, song_id):
        content = self.send('http://music.163.com/song?id={}'.format(song_id))

        dict_re = {
            'play_list_img': r'src="([^\?]+\?param=50y50)"',
            'play_list': r'f-fs1 s-fc0" href="/playlist\?id=(\d+)" title="([^"]+)',
            'play_list_artist': r'/user/home\?id=(\d+)" title="([^"]+)',
            'sim_1': r'f-thide">\n<a href="/song\?id=(\d+)" title="([^"]+)"',
            'sim_2': r'f-thide s-fc4"><span title="([^"]+)'
        }

        def find(name):
            return re.findall(dict_re.get(name), content)

        music_list = []
        self.add_list(self.playlist_map(find('play_list'), find('play_list_img'), find('play_list_artist')), music_list, self.list_name[3])
        self.add_list(self.map_list(find('sim_1'), find('sim_2'), 2), music_list, self.list_name[0])
        return music_list

    ''' 爬取歌单详情 '''
    def playlist_detail(self, playlist_id):
        data = json.loads(self.send('http://music.163.com/api/playlist/detail?id={}'.format(playlist_id)))['result']
        content = self.send('http://music.163.com/playlist?id={}'.format(playlist_id))

        dict_re = {
            'creator_info': r'user/home\?id=(\d+)"><img src="([^\?]+\?param=40y40)',
            'date': r'time s-fc4">([^&]+)&nbsp',
            'creator_name': r's-fc7">([^<]+)',
            'play_list_img': r'src="([^\?]+\?param=50y50)"',
            'play_list': r'f-fs1 s-fc0" href="/playlist\?id=(\d+)" title="([^"]+)',
            'play_list_artist': r'/user/home\?id=(\d+)" title="([^"]+)',
            'user': r'user/home\?id=(\d+)" class="f-tdn" title="([^"]+)"\n><img src="([^\?]+)\?param=40y40'
        }

        def find(name):
            return re.findall(dict_re.get(name), content)

        info = find('creator_info')[0]
        return_list = []

        return_list.append({
            'img': data['coverImgUrl'],
            'name': data['name'],
            'description': data['description'],
            'creator_id': info[0],
            'creator_img': info[1],
            'creator': find('creator_name')[0],
            'date': find('date')[0]
        })
        agency_list = []
        for i in data['tracks']:
            agency_list.append({
                'name': i.get('name'),
                'id': i.get('id'),
                'artist': i.get('artists')[0].get('name'),
                'album': i.get('album').get('name')
            })
        return_list.append(agency_list)
        self.add_list(self.playlist_map(find('play_list'), find('play_list_img'), find('play_list_artist')), return_list, self.list_name[3])
        self.add_list(find('user'), return_list, self.list_name[0])
        return return_list

    def album_detail(self, album_id):
        content = self.send('http://music.163.com/album?id={}'.format(album_id))
        return_list = []

        dict_re = {
            'song': r'song\?id=(\d+)">([^<]+)',
            'album': r'f-ff2">([^<]+)',
            'artist': r'artist\?id=(\d+)" >([^<]+)',
            'date': r'间：</b>([^<]+)',
            'company': r'司：</b>\n([^\n]+)',
            'user': r'user/home\?id=(\d+)" class="f-tdn" title="([^"]+)"\n><img src="([^\?]+)\?param=40y40',
            'album_info': r'album\?id=(\d+)" title="([^"]+)">\n<img src="([^\?]+)\?param=50y50',
            'album_date': r'<p class="s-fc3">([^<]+)',
            'img': r'images": \["([^"]+)',
            'more': '(album-desc-more)',
            'description': '(n-albdesc)'
        }

        def find(name):
            return re.findall(dict_re.get(name), content)

        album_name, title = find('album')[: 2]
        artist = find('artist')[0]
        if find('more'):
            description = BeautifulSoup(content, 'lxml').find_all(id='album-desc-more')[0].get_text()
        elif find('description'):
            description = BeautifulSoup(content, 'lxml').find_all(class_='n-albdesc')[0].find_all(class_='f-brk')[0].get_text()
        else:
            description = '无'

        return_list.append({
            'artist_id': artist[0],
            'artist_name': artist[1],
            'date': find('date')[0],
            'company': find('company')[0],
            'album_name': album_name,
            'title': title,
            'img': find('img')[0],
            'description': description
        })
        self.add_list(find('user'), return_list, self.list_name[0])
        self.add_list(self.map_list(find('album_info'), find('album_date'), 3), return_list, self.list_name[1])
        self.add_list(find('song'), return_list, self.list_name[0])
        return return_list

    def artist_detail(self, artist_id, category=None):
        urls = {
            'album': 'http://music.163.com/artist/album?id={}',
            'description': 'http://music.163.com/artist/desc?id={}',
            'null': 'http://music.163.com/artist?id={}'
        }
        content = self.send((urls[category] if category else urls['null']).format(artist_id))
        result_list = []

        info = re.findall(r'f-thide" title="([^"]+)">\n', content)[0].split('-')
        img = re.findall(r'src="([^\?]+)\?param=640y300"', content)[0]
        artist = re.findall(r'artist\?id=(\d+)" title="([^"]+)">\n<img src="([^\?]+)\?param=50y50', content)

        result_list.append({
            'name': info[0],
            'title': info[1],
            'img': img,
            'id': artist_id,
            'hot_singer': [dict(zip(self.list_name[0], i)) for i in artist]
        })

        if category == 'description':
            soup = BeautifulSoup(content, 'lxml').find_all(class_='n-artdesc')[0]
            detail = [re.sub(r'<[/]?p([^>]*)>', '', str(_)).split('<br/>') for _ in soup.find_all('p')]
            title = soup.find_all('h2')
            result_list.append([{'title': re.sub(r'\xa0', '', title[i].get_text()), 'detail': detail[i]} for i in range(len(title))])
        elif category == 'album':
            info = re.findall(r'"([^"]+)">\n<img src="([^\?]+)\?param=120y120"/>\n<a href="/album\?id=(\d+)', content)
            date = re.findall(r's-fc3">([^<]+)', content)
            self.add_list(self.map_list(info, date, 3), result_list, self.list_name[1])
        else:
            songs = re.findall(r'song\?id=(\d+)">([^<]+)', content)
            self.add_list(songs, result_list, self.list_name[2])
        return result_list

    ''' 爬取云音乐用户界面 '''
    def user_detail(self, user_id):
        data = json.loads(self.send('http://music.163.com/api/user/playlist/?offset={}&limit={}&uid={}'.format(0, 100, user_id)))['playlist']
        content = self.send('http://music.163.com/user/home?id={}'.format(user_id))
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
            return re.findall(dict_re[name], content)[0]

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

        return return_list

    ''' 爬取云音乐排行榜 '''
    def top_list_detail(self, id=None):
        url = 'http://music.163.com/discover/toplist'
        if id:
            url += '?id={}'.format(id)
        content = self.send(url)
        return_list = []

        dict_re = {
            'info': r'(\d+)" class="s-fc0">([^<]+)</a></p>\n<p class="s-fc4">([^<]+)',
            'img': r'src="([^\?]+)\?param=40y40',
            'the_img': r'src="([^\?]+)\?param=150y150',
            'the_info': r'f-ff2">([^<]+)</h2>\n</div>\n<div class="user f-cb">\n<i class="u-icn u-icn-57"></i><span class="sep s-fc3">最近更新：([^<]+)</span> <span class="s-fc4">([^<]+)',
            'songs': r'/song\?id=(\d+)">([^<]+)',
            'artists': r'artists":\[{"id":\d+,"name":"([^"]+)","tns'
        }

        def find(name):
            return re.findall(dict_re[name], content)

        top_lists = self.map_list(find('info'), find('img'), 3)
        self.add_list(self.map_list(find('the_info'), find('the_img'), 3), return_list, self.list_name[1])
        self.add_list(top_lists[: 4], return_list, self.list_name[1])
        self.add_list(top_lists[4:], return_list, self.list_name[1])
        self.add_list(self.map_list(find('songs'), find('artists'), 2), return_list, self.list_name[0])
        return return_list

    ''' 通过输入歌曲名搜索音乐 '''
    def search_song(self, name, type='1', limit=30):
        song_list = []
        if not name:
            return song_list
        url = 'http://music.163.com/api/search/pc'
        data = {
            's': name,
            'offset': 0,
            'limit': limit,
            'type': type,
            'total': 'true'
        }
        for _ in self.send(url, data).get('result').get('songs'):
            song_list.append({
                'name': _['name'],
                'id': _['id'],
                'artist': _['artists'][0]['name'],
                'album': _['album']['name']
            })
        return song_list

    def dj_detail(self, id):
        content = self.send('http://music.163.com/dj?id={}'.format(id))
        return_list = []
        dict_re = {
            'id': r'R_SO_4_(\d+)',
            'cover_img': r'coverUrl":"([^"]+)',
            'info': r'program\?id=(\d+)" title="([^<]+)">[^<]+</a></p>\n<p><span class="by s-fc4">([^<]+)',
            'imgs': r'src="([^\?]+\?param=50y50)',
        }

        def find(name):
            return re.findall(re.compile(dict_re[name]), content)

        return_list.append({
            'music_id': find('id')[0],
            'cover_img': find('cover_img')[0]
        })
        self.add_list(self.map_list(find('info'), find('imgs'), 3), return_list, self.list_name[1])
        return return_list

    ''' 音乐播放界面的展示图片，爬虫自图虫网 '''
    def get_background(self, song):
        url = 'https://stock.tuchong.com/free/search/?term={}'.format(quote(song))
        ids = re.findall(re.compile(r'imageId":"(\d+)'), self.send(url))
        if ids:
            return 'https://p3a.pstatp.com/weili/l/{}.jpg'.format(choice(ids))
        return 'http://photos.tuchong.com/339151/f/22354551.jpg'

    def shi(self):
        from lxml import etree

        content = self.send('http://music.163.com/discover/toplist?id=3779629')
        data = etree.HTML(content)
        x = data.xpath('//ul[@class="f-hide"]/li')
        for i in x:
            href = i.xpath('./a/@href')[0]
            id = re.findall(re.compile(r'(\d+)'), href)[0]
            name = i.xpath('./a/text()')[0]
            print(name)

if __name__ == '__main__':
    ym = Yun_Music()
    # with open('{}json/new_top_list.json'.format(Methods.absolute_path), 'r', encoding='utf-8') as f:
    #     t = f.read()
    # # f.close()
    # print(type(t))
    # for i in ym.get_play_list():
    for j in ym.get_play_list()[1]:
        print(j)


