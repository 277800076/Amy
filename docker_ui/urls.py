#! /usr/bin/env python
# coding=utf-8
from django.conf.urls import include, url
from views import RegistryAdd, RegistryApi, RegistryList

urlpatterns = [
    url(r'^registry/add$', view=RegistryAdd.as_view(), name='docker_registry'),
    url(r'^registry/$', view=RegistryList.as_view(), name='docker_registry'),
    url(r'^registry/$', view=RegistryApi.as_view(), name='docker_registry'),
]
