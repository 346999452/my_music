#! usr/bin/env python
#-*- coding=utf-8 -*-
"""

    @author: 南辙一曲风华顾
    @file: fan_middle
    @date: 2018/06/26
    
"""
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

class fan_user_agent_middleware(MiddlewareMixin):
    def process_request(self, request):
        http_user_agent = request.META.get('HTTP_USER_AGENT')
        # remote_addr = request.META.get('REMOTE_ADDR')
        http_user_agent = str(http_user_agent).lower()

        if "py" in http_user_agent or "ssl" in http_user_agent:
            return render(request, 'template.html')
        return None

    def process_response(self, request, response):
        return response