# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: admin
    @time: 2018/04/05

"""

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(lunbo_model)
admin.site.register(commend_model)
admin.site.register(new_model)
admin.site.register(rank_model)
admin.site.register(singer_model)
admin.site.register(movie_model)
admin.site.register(user_comment)


