# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: __init__
    @time: 2018/05/06

"""
from scrapy import cmdline
from other_class.methods import Methods

def setup_django_env():
    import os, django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_music.settings")
    django.setup()

def check_db_connection():
    from django.db import connection

    if connection.connection:
        if not connection.is_usable():
            connection.close()

setup_django_env()
check_db_connection()
# cmdline.execute('scrapy crawl nfy'.split())
# cmdline.execute('scrapy crawl user'.split())
# cmdline.execute('scrapy crawl top_list'.split())
# cmdline.execute('scrapy crawl play_list'.split())
# cmdline.execute('scrapy crawl exam'.split())




