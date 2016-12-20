#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Registry, LogServer
from layui.api import RestApi
from layui.views import LayUiTableViews, LayUiFormViews
from forms import RegistryForm, LogServerForm, CreateDockerContainerForm, ContainerTemplateForm, ImageFrom, OptionForm
from actions import DeleteRegistry, CreateRegistryBtn
from actions import DeleteLogServer, CreateLogServerBtn


class RegistryTableViews(LayUiTableViews):
    model = Registry
    name = u'仓库'
    action = [DeleteRegistry]
    btn = [CreateRegistryBtn]


class RegistryApi(RestApi):
    models = Registry


class RegistryFormViews(LayUiFormViews):
    form_class = RegistryForm
    ajax_url = '/api/docker/registry/'
    form_name = u'新增仓库'


class LogServerViews(LayUiTableViews):
    model = LogServer
    name = u'日志服务'
    action = [DeleteLogServer]
    btn = [CreateLogServerBtn]


class LogServerApi(RestApi):
    models = LogServer


class LogServerFormViews(LayUiFormViews):
    form_class = LogServerForm
    ajax_url = '/api/docker/log/'
    form_name = u'新增仓库'


class CreateDockerContainerFormViews(LayUiFormViews):
    form_class = CreateDockerContainerForm
    ajax_url = ''
    form_name = u'创建容器'


class DockerTemplateFormViews(LayUiFormViews):
    form_class = ContainerTemplateForm
    ajax_url = ''
    form_name = u'创建模版'


class DockerImageFromViews(LayUiFormViews):
    form_class = ImageFrom
    ajax_url = ''
    form_name = u'创建镜像'


class OptionFormViews(LayUiFormViews):
    form_class = OptionForm
    ajax_url = ''
    form_name = u'新增参数'