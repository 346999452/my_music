# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: __init__
    @time: 2018/05/06

    管道
    一般用于存储数据为文件或者入库
    See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""

class NfyPipeline(object):
    def process_item(self, item, spider):
        try:
            item.save()
        except:
            pass
        return item