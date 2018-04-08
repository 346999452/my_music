# ! usr/bin/env python
# -*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: models
    @time: 2018/04/05

"""

from django.db import models

class user(models.Model):
    username = models.CharField(max_length=32)
    loginname = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __str__(self):
        return '{} | {}'.format(self.username, self.password)
