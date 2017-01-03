#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Registry, LogServer, DockerImages, DockerHost, DockerTemplateOption, DockerContainerModels
from models import DockerTemplate
from layui.views import RestApi
from actions import TemplateOptionAction, TemplateOptionShow
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.conf.urls import url, patterns
from forms import RegistryForm, LogServerForm, ImageFrom, CreateDockerContainerForm
from forms import DockerHostAddForm, DockerTemplateForm, DockerTemplateOptionForm
from addict import Dict
from layui.actions import JSAction, BtnShow
from actions import DockerContainerShow
import time


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


class DockerTemplateOptionApi(RestApi):
    name = u'模板参数'
    list_display = ('key', 'value')
    form_class = DockerTemplateOptionForm
    form_name = u'模板参数'
    models = DockerTemplateOption

    def get_queryset(self, request, *args, **kwargs):
        template_id = args[0]
        template = DockerTemplate.objects.get(pk=template_id)
        return self.models.objects.filter(template=template)

    def _get_btn(self, *args, **kwargs):
        return None

    @classmethod
    def urls(cls):
        urlpatterns = patterns(
            '',
            url(r'api/%s/%s/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.as_view(),
                name=cls.__name__),
            url(r'api/%s/%s/(.+)/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.as_view(),
                name=cls.__name__),
            url(r'%s/%s/create/(.+)/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.form,
                name=cls.__name__),
            url(r'%s/%s/(.+)/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.table,
                name=cls.__name__)
        )
        return urlpatterns


class DockerHostApi(RestApi):
    name = u'主机'
    form_class = DockerHostAddForm
    form_name = u'创建主机'
    models = DockerHost
    action = [DockerContainerShow]


class DockerTemplateApi(RestApi):
    name = u'模版'
    form_class = DockerTemplateForm
    form_template = 'template_add.html'
    form_name = u'创建模版'
    models = DockerTemplate
    action = [TemplateOptionAction, TemplateOptionShow]


class DockerContainerView(RestApi):
    list_display = ('Id', 'Names', 'Image', 'Ports', 'State', 'Status')
    exclude_field = ('NetworkSettings', 'ImageID', 'Labels', 'Command', 'HostConfig', 'Mounts')
    models = DockerContainerModels
    name = u'容器'
    form_class = CreateDockerContainerForm
    form_name = u'新增容器'

    def _get_order(self):
        if self.order:
            return self._get_list_display.index(self.order)
        else:
            return 0

    def get_queryset(self, request, host_id, **kwargs):
        docker = self._docker(host_id)
        query = docker.containers()
        del docker
        return query

    def _get_td(self, request, docker, **kwargs):
        _html = u''
        for obj in docker.containers():
            obj = Dict(obj)
            _td = ''.join([self._format_value(obj, _field)
                           for _field in self._get_list_display if hasattr(obj, _field)])

            actions = [act(request, obj) for act in self.action]
            actions.append(JSAction(request, obj, **{'action_type': 'delete', 'icon': 'fa fa-trash'}))

            _td += u'<td>{}</td>'.format(''.join([act.__html__() for act in actions]))
            _html += u'<tr>{}</tr>'.format(_td)
        return _html

    def get_context_data(self, request, *args, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        host_id = args[0]
        docker = self._docker(host_id)
        kwargs['table_th'] = self._table_th()
        kwargs['table_td'] = self._get_td(request, docker, **kwargs)
        kwargs['order'] = self._get_order()
        kwargs['btns'] = self._get_btn(host_id, *args, **kwargs)
        del docker
        return kwargs

    def _get_btn(self, host_id, *args, **kwargs):
        _btn = [{
            'open_url': '/%s/%s/create/?host=%s' % (self.models._meta.app_label, self.models._meta.model_name, host_id),
            'name': u'添加' + self.get_name(),
        }]

        self.btn = self.btn + _btn
        return [BtnShow(**data).__html__() for data in self.btn]

    def _format_value(self, value, _field):
        if _field == 'Ports':
            values = getattr(value, _field)
            _html = ' '.join([u'{}=>{}'.format(value.PublicPort, value.PrivatePort) for value in values])
        elif _field == 'Id':
            _html = getattr(value, _field)[0:12]
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
        return DockerHost.objects.get(pk=int(host)).docker_cli

    @classmethod
    def urls(cls):
        urlpatterns = patterns(
            '',
            # url(r'api/%s/%s/(.+)/(.+)/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.as_view(),
            #     name=cls.__name__),
            url(r'api/%s/%s/(.+)/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.as_view(),
                name=cls.__name__),
            url(r'%s/%s/create/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.form,
                name=cls.__name__),
            url(r'%s/%s/(.+)/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.table,
                name=cls.__name__)
        )
        return urlpatterns

    def get_api_url(self, request, *args, **kwargs):
        return r'/api/%s/%s/%s/' % (self.models._meta.app_label, self.models._meta.model_name, request.GET.get('host'))

    def get(self, request, host_id=None, *args, **kwargs):
        return JsonResponse(data=self._success_msg(None), safe=False)

    def post(self, request, host_id=None, *args, **kwargs):
        docker = self._docker(host_id)
        _data = Dict(request.POST.dict())
        del docker
        try:
            self._container_config(_data)
            return JsonResponse(data=self._success_msg(None), safe=False)
        except Exception, e:
            return JsonResponse(data=self._failure_msg(str(e)), safe=False)

    def _container_config(self, _data):
        template = DockerTemplate.objects.get(pk=_data.template)
        config = template.config()
        registry = template.registry()
        image = template.image()
        if _data.custom:
            custom = {i.split('=')[0]: i.split('=')[1] for i in str(_data.custom).split(',')}
        else:
            custom = {}
        print custom, config, registry, image

    def put(self, request, host_id=None, *args, **kwargs):
        pass

    def delete(self, request, host_id=None, *args, **kwargs):
        pass
