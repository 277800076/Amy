#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Registry, LogServer, DockerImages, DockerHost, DockerTemplateOption
from layui.views import RestApi
from django.http import JsonResponse
from django.shortcuts import render_to_response
from addict import Dict
from django.conf.urls import include, url, patterns
from forms import RegistryForm, LogServerForm, CreateDockerContainerForm, ContainerTemplateForm, ImageFrom, OptionForm
from forms import DockerHostAddForm, DockerTemplateOptionForm
from actions import TemplateOptionAction
from layui.actions import BtnShow


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

    def _post(self, **kwargs):
        data = Dict(kwargs)
        registry = Registry.objects.get(pk=data.pop('registry'))
        data['registry'] = registry
        return data

    def post(self, request, data_id=None, *args, **kwargs):
        try:
            post = {v: self.format_json(request.POST.dict()[v]) for v in request.POST.dict()}
            data = self.models(**self._post(**post))
            data.save()
            return JsonResponse(data=self._success_msg(None), safe=False)
        except Exception, e:
            return JsonResponse(data=self._failure_msg(str(e)))


class DockerHostApi(RestApi):
    name = u'主机'
    form_class = DockerHostAddForm
    form_name = u'创建主机'
    models = DockerHost


class DockerTemplateOptionApi(RestApi):
    name = u'模版'
    form_class = DockerTemplateOptionForm
    form_name = u'创建模版'
    models = DockerTemplateOption

    def save(self, request):
        print request.POST.dict()
        print self.models._meta.local_fields

    def post(self, request, data_id=None, *args, **kwargs):
        self.save(request)
        try:
            post = {v: self.format_json(request.POST.dict()[v]) for v in request.POST.dict()}
            data = self.models(**post)
            data.save()
            return JsonResponse(data=self._success_msg(None), safe=False)
        except Exception, e:
            print e
            return JsonResponse(data=self._failure_msg(str(e)))
