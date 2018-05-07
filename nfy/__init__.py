# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: __init__
    @time: 2018/05/06

"""

# with open('./file/htm/htm1', 'rb') as f:
#     print(f.read().decode('utf-8'))


from scrapy import cmdline

cmdline.execute('scrapy crawl nfy'.split())



