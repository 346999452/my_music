# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: yun_music
    @time: 2018/01/30
    
"""
from other_class.http_client import Http_Client
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from other_class.methods import Methods
import base64, json, re
from urllib.request import quote

class Yun_Music(Methods, Http_Client):

    def __init__(self):
        Http_Client.__init__(self)
        self.set_header()
        self.top_list_urls = self.get_json('config/top_list.json')

        ''' 映射字典的key值(共用) '''
        self.list_name = [
            ['id', 'name', 'rank'],
            ['singer', 'identity', 'img', 'id'],
            ['img', 'url'],
            ['id', 'name', 'artist', 'artist_id', 'img']
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
            return

    ''' 通过输入歌曲名搜索音乐 '''
    def search_song(self, name):
        url = 'http://music.163.com/api/search/pc'
        data = {
            's': name,
            'offset': 0,
            'limit': 20,
            'type': "1"
        }
        song_list = []
        for _ in self.send(url, data).get('result').get('songs'):
            song_list.append((_['name'], _['id'], _['artists'][0]['name'], _['album']['name']))
        return song_list

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
        music_list = list(map(lambda x, y: (x[0], x[1], y), self.get_top_list(list_name)[: 10], [i + 1 for i in range(10)]))
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
    
    @staticmethod
    def add_list(list, song_list, list_name):
        agency_list = []
        for i in list:
            agency_list.append(dict(zip(list_name, i)))
        song_list.append(agency_list)

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
        self.add_list(list(map(lambda x, y: (x[0], '电台节目' if x[1] == 'dj' else '歌单', x[2], y), find('play_list'), find('play_list_img'))), song_list, self.list_name[1])

        ''' 轮播图 '''
        self.add_list(find('lunbo'), song_list, self.list_name[2])

        ''' 新碟上架 '''
        self.add_list(list(map(lambda x, y: (x[2], x[1], y[0], y[1], x[0]), find('album_list')[: 10], find('album_list_artist')[: 10])), song_list, self.list_name[3])

        return song_list

    def get_play_list(self, play_list_name=None):
        if play_list_name:
            content = self.send('http://music.163.com/discover/playlist/?cat={}'.format(quote(play_list_name)))
        else:
            content = self.send('http://music.163.com/discover/playlist')
        info = re.findall(r'title="([^"]+)" href="/playlist\?id=(\d+)" class="tit f-thide s-fc0">([^<]+)</a>\n</p>\n<p><span class="s-fc4">by</span> <a title="([^"]+)', content)
        img = re.findall(r'src="([^\?]+\?param=140y140)"', content)
        play_list = []
        for i in list(map(lambda x, y: (x[1], x[0], x[3], y), info, img)):
            play_list.append(dict(zip(self.list_name[1], i)))
        return play_list

    ''' 获取音乐歌词 '''
    def get_lyric(self, song_id):
        url = 'http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
        data = json.loads(self.send(url))
        lyric_list = []
        for i in (data['lrc']['lyric'] + ('\n' + data['tlyric']['lyric'] if data['tlyric']['lyric'] else '')).split('\n'):
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
            'similar_music': r'(\d+)"\n>([^<]+)</a>\n</div>\n<div class="f-thide s-fc4"><span title="([^"]+)'
        }

        def find(name):
            return re.findall(dict_re.get(name), content)

        music_list = []
        self.add_list(list(map(lambda x, y, z: (x[0], x[1], y, z[0], z[1]),
                               find('play_list'), find('play_list_img'),
                               find('play_list_artist'))), music_list, self.list_name[3])
        self.add_list(find('similar_music'), music_list, self.list_name[0])
        return music_list

if __name__ == '__main__':
    ym = Yun_Music()
    print(ym.get_play_list())
    # print(ym.get_music_src('550138132'))
