#! /usr/bin/env python
# coding=utf-8
from django.conf import settings
from django.http import HttpResponseRedirect


class AuthLoginMiddleware(object):
    def process_request(self, request):
        if request.path != settings.LOGIN_URL:
            if not request.user.is_authenticated():
                return HttpResponseRedirect(settings.LOGIN_URL)