#!usr/bin/env python
#-*- coding:utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: forms
    @time: 2017/11/18

"""
from .models import user
from django import forms

class user_form(forms.ModelForm):
    class Meta:
        model = user

        fields = ['username', 'loginname', 'password']
