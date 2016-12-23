#! /usr/bin/env python
# coding=utf-8
from django.conf.urls import include, url
from views import RegistryApi, LogServerApi, ImageApi, DockerHostApi, DockerTemplateOptionApi

urlpatterns = [
    url(r'^', include(RegistryApi.urls())),
    url(r'^', include(LogServerApi.urls())),
    url(r'^', include(ImageApi.urls())),
    url(r'^', include(DockerHostApi.urls())),
    url(r'^', include(DockerTemplateOptionApi.urls())),
]
