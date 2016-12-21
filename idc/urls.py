#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from views import TestRestApi

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^', include('amy.urls')),
    # url(r'^', include('docker_ui.urls')),
    url(r'^', include(TestRestApi.urls())),
]
