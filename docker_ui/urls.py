#! /usr/bin/env python
# coding=utf-8
from django.conf.urls import include, url
from views import RegistryTableViews, RegistryApi, RegistryFormViews
from views import LogServerFormViews, LogServerApi, LogServerViews
from views import CreateDockerContainerFormViews, DockerTemplateFormViews, DockerImageFromViews, OptionFormViews

urlpatterns = [
    url(r'^docker/registry/$', view=RegistryTableViews.as_view(), name='docker_registry'),
    url(r'^docker/registry/create/$', view=RegistryFormViews.as_view(), name='docker_registry_create'),
    url(r'^api/docker/registry/$', view=RegistryApi.as_view(), name='rest_registry'),
    url(r'^api/docker/registry/(.+)/$', view=RegistryApi.as_view(), name='rest_registry'),

    url(r'^docker/log/$', view=LogServerViews.as_view(), name='docker_logserver'),
    url(r'^docker/log/create/$', view=LogServerFormViews.as_view(), name='docker_logserver_create'),
    url(r'^api/docker/log/$', view=LogServerApi.as_view(), name='rest_logserver'),
    url(r'^api/docker/log/(.+)/$', view=LogServerApi.as_view(), name='rest_logserver'),

    url(r'^docker/container/create/$', view=CreateDockerContainerFormViews.as_view(), name='docker_container_create'),
    url(r'^docker/template/create/$', view=DockerTemplateFormViews.as_view(), name='docker_template_create'),
    url(r'^docker/images/create/$', view=DockerImageFromViews.as_view(), name='docker_images_create'),
    url(r'^docker/option/create/$', view=OptionFormViews.as_view(), name='docker_option_create'),
]
