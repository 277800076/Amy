#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Registry, LogServer, DockerImages, DockerHost, DockerTemplateOption
from layui.views import RestApi
from django.views.generic import TemplateView
from forms import RegistryForm, LogServerForm, ImageFrom
from forms import DockerHostAddForm, DockerTemplateOptionForm
from addict import Dict
from hashers.docker.client import Docker
from layui.actions import JSAction
import time


docker_container_models = Dict({
    '_meta': {
        'model_name': 'docker',
        'app_label': 'docker_ui',
        'local_fields': [
            {'name': u'Status', 'verbose_name': u'启动时间'},
            {'name': u'Created', 'verbose_name': u'创建时间'},
            {'name': u'Image', 'verbose_name': u'镜像'},
            {'name': u'Labels', 'verbose_name': u'标签'},
            {'name': u'NetworkSettings', 'verbose_name': u'网络'},
            {'name': u'HostConfig', 'verbose_name': u'配置'},
            {'name': u'ImageID', 'verbose_name': u'镜像ID'},
            {'name': u'State', 'verbose_name': u'状态'},
            {'name': u'Command', 'verbose_name': u'命令'},
            {'name': u'Names', 'verbose_name': u'容器名称'},
            {'name': u'Mounts', 'verbose_name': u'卷组'},
            {'name': u'Id', 'verbose_name': u'容器ID'},
            {'name': u'Ports', 'verbose_name': u'端口'}
        ]
    }
})


class RegistryApi(RestApi):
    name = u'仓库'
    form_class = RegistryForm
    form_name = u'新增仓库'
    models = Registry


class LogServerApi(RestApi):
    name = u'日志'
    form_class = LogServerForm
    form_name = u'新增日志'
    models = LogServer


class ImageApi(RestApi):
    name = u'镜像'
    form_class = ImageFrom
    form_name = u'新增镜像'
    models = DockerImages


class DockerHostApi(RestApi):
    name = u'主机'
    form_class = DockerHostAddForm
    form_name = u'创建主机'
    models = DockerHost


class DockerTemplateOptionApi(RestApi):
    name = u'模版'
    form_class = DockerTemplateOptionForm
    form_template = 'template_add.html'
    form_name = u'创建模版'
    models = DockerTemplateOption


class DockerContainerView(RestApi):
    list_display = ('Id', 'Names', 'Image', 'Ports', 'State')
    exclude_field = ('NetworkSettings', 'ImageID', 'Labels', 'Command', 'HostConfig', 'Mounts')
    models = docker_container_models
    name = u'容器信息'

    def _get_order(self):
        if self.order:
            return self._get_list_display.index(self.order)
        else:
            return 0

    def get_context_data(self, request, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        docker = self._docker(kwargs['host'])
        kwargs['docker_list'] = docker.containers_list(all=True)
        kwargs['table_th'] = self._table_th()
        kwargs['table_td'] = self._get_td(request, docker)
        kwargs['order'] = self._get_order()
        del docker
        return kwargs


    def _format_value(self, value, _field):
        if _field == 'Ports':
            values = getattr(value, _field)
            _html = ' '.join([u'{}=>{}'.format(value.PublicPort, value.PrivatePort) for value in values])
        elif _field == 'Id':
            _html = getattr(value, _field)[0:9]
        elif _field == 'Created':
            value = time.localtime(getattr(value, _field))
            _html = time.strftime('%Y-%m-%d %H:%M:%S', value)
        elif _field == 'Names':
            _html = str(getattr(value, _field)[0]).lstrip('/')
        elif _field == 'State':
            values = getattr(value, _field)
            if values == 'running':
                _html = u'<i class="layui-btn layui-btn-mini">{}</i>'.format(values)
            else:
                _html = u'<i class="layui-btn layui-btn-mini layui-btn-danger">{}</i>'.format(values)
        else:
            _html = str(getattr(value, _field))
        return u'<td>{}</td>'.format(_html)

    def _docker(self, host):
        docker_host = DockerHost.objects.get(pk=int(host))
        base_url = docker_host.base_url
        return Docker(base_url)