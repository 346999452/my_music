# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: admin
    @time: 2018/04/05

"""

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(user)
admin.site.register(music_info)
admin.site.register(album_info)
admin.site.register(playlist_info)
admin.site.register(music_collec)
admin.site.register(album_collec)
admin.site.register(playlist_collec)

