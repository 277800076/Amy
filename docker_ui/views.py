#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Registry, LogServer, DockerImages, DockerContainerTemplate, DockerContainerOption
from layui.views import RestApi
from django.http import JsonResponse
from django.shortcuts import render_to_response
from addict import Dict
from django.conf.urls import include, url, patterns
from forms import RegistryForm, LogServerForm, CreateDockerContainerForm, ContainerTemplateForm, ImageFrom, OptionForm
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


class TemplateApi(RestApi):
    name = u'模版'
    form_class = ContainerTemplateForm
    form_name = u'创建模版'
    models = DockerContainerTemplate
    action = [TemplateOptionAction]

    def _post(self, **kwargs):
        data = Dict(kwargs)
        images = DockerImages.objects.get(pk=data.pop('images'))
        data['images'] = images
        return data

    def post(self, request, data_id=None, *args, **kwargs):
        try:
            post = {v: self.format_json(request.POST.dict()[v]) for v in request.POST.dict()}
            data = self.models(**self._post(**post))
            data.save()
            return JsonResponse(data=self._success_msg(None), safe=False)
        except Exception, e:
            return JsonResponse(data=self._failure_msg(str(e)))


class TemplateOptionApi(RestApi):
    name = u'模版参数'
    form_class = OptionForm
    form_name = u'创建模版'
    models = DockerContainerOption

    def _post(self, **kwargs):
        data = Dict(kwargs)
        container = DockerContainerTemplate.objects.get(pk=data.pop('container'))
        data['container'] = container
        return data

    def post(self, request, data_id=None, *args, **kwargs):
        try:
            post = {v: self.format_json(request.POST.dict()[v]) for v in request.POST.dict()}
            post['container'] = data_id
            data = self.models(**self._post(**post))
            data.save()
            return JsonResponse(data=self._success_msg(None), safe=False)
        except Exception, e:
            return JsonResponse(data=self._failure_msg(str(e)))

    def get(self, request, template_id=None, *args, **kwargs):
        if template_id is None:
            return JsonResponse(data=self._failure_msg(u'No specified template ID'), safe=False)
        else:
            try:
                data_id = int(template_id)
                data = [self.models.objects.values(*self._list_display).get(id=data_id)]
                return JsonResponse(data=self._success_msg(data), safe=False)
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)), safe=False)

    def get_context_data(self, request, *args, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['table_td'] = self._get_td(request, *args, **kwargs)
        kwargs['table_th'] = self._table_th()
        kwargs['order'] = self._get_order()
        kwargs['btns'] = self._get_btn(*args, **kwargs)
        return kwargs

    def get_queryset(self, *args, **kwargs):
        return self.models.objects.filter(container=args[0])

    @classmethod
    def table(cls, request, *args, **kwargs):
        context = cls().get_context_data(request, *args, **kwargs)
        return render_to_response(template_name=cls.table_template, context=context)

    def _get_btn(self, *args, **kwargs):
        _btn = [{
            'open_url': '/%s/%s/create/%s' % (self.models._meta.app_label, self.models._meta.model_name, args[0]),
            'name': u'添加' + self.get_name(),
        }]

        self.btn = self.btn + _btn
        return [BtnShow(**data).__html__() for data in self.btn]

    @classmethod
    def form(cls, request, *args, **kwargs):
        context = {
            'form': cls.form_class(),
            'view': cls,
            'api_url': cls().get_api_url().rstrip('/') + '/' + args[0] + '/'
        }
        return render_to_response(template_name=cls.form_template, context=context)

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

