# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: tasks.py
    @time: 2018/05/03
    
"""
import requests
from celery import Celery
from other_class.methods import Methods

app = Celery('image_downloader', broker='amqp://guest:guest@localhost:5672//')

@app.task
def download_pic(image_url, image_path):
    """
        异步下载图片

        Args:
            image_url (string): 图片链接
            image_path (string): 图片路径
    """
    image_path = Methods.absolute_path + '/image/image/' + image_path

    if not (image_url and image_path):
        print('非法路径')

    try:
        image = requests.get(image_url, stream=True)
        with open(image_path, 'wb') as img:
            img.write(image.content)
    except Exception as exc:
        print(exc)

if __name__ == '__main__':
    download_pic('http://p1.music.126.net/zLGAFoywT_Hwon4KxR11yQ==/109951163279541917.jpg', '1.jpg')