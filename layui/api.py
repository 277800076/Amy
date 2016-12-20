#! /usr/bin/env python
# coding=utf-8
from django.db.models import Model
from amy.models import Menus
from django.views.generic import View
from django.http import JsonResponse, QueryDict
from django.forms import model_to_dict
from django.conf.urls import include, url, patterns


class RestViewMixin(object):
    models = None
    allowed_method = ['get', 'post', 'get', 'delete', 'option']
    exclude_field = ()

    def __init__(self, models=None, method=None):
        self.http_method_names = self._method(method)
        if models is not None:
            self.models = self._models(models)

    def _success_msg(self, data):
        return {'result': 'success', 'data': data}

    def _failure_msg(self, code):
        return {'result': 'failure', 'code': code}

    def _models(self, models):
        assert models.__class__ == Model.__class__
        return models

    def _method(self, method):
        """
        method 不能为空集或者字符串
        :param method: 必须在 allowed_method 中
        :return: 与 allowed_method的交集
        """
        if method is None:
            return self.allowed_method
        assert type(method) == list and method
        return [str(i).lower() for i in method if i.lower() in self.allowed_method]

    @property
    def query_set(self):
        return self.models.objects.all()

    @property
    def _list_display(self):
        return [field.name for field in self.models._meta.local_fields if field.name not in self.exclude_field]

    def get(self, request, data_id=None, *args, **kwargs):
        if data_id is None:
            try:
                data = [data for data in self.models.objects.values(*self._list_display)]
                return JsonResponse(data=self._success_msg(data), safe=False)
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)), safe=False)
        else:
            try:
                data_id = int(data_id)
                data = [self.models.objects.values(*self._list_display).get(id=data_id)]
                return JsonResponse(data=self._success_msg(data), safe=False)
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)), safe=False)

    def post(self, request, data_id=None, *args, **kwargs):
        try:
            post = {v: self.format_json(request.POST.dict()[v]) for v in request.POST.dict()}
            data = self.models(**post)
            data.save()
            return JsonResponse(data=self._success_msg(None), safe=False)
        except Exception, e:
            return JsonResponse(data=self._failure_msg(str(e)))

    def put(self, request, data_id=None, *args, **kwargs):
        if data_id is None:
            return JsonResponse(data=self._failure_msg(u'No specified data ID'))
        else:
            try:
                data_id = int(data_id)
                data = self.query_set.get(id=data_id)
                put = QueryDict(request.body, encoding=request.encoding)
                data.update(**put).save()
                # data = self.query_set.get(id=data_id)
                # data.update(**request.POST)
                return JsonResponse(data=self._success_msg(data=None))
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)))

    def delete(self, request, data_id=None, *args, **kwargs):
        if data_id is None:
            return JsonResponse(data=self._failure_msg(u'No specified data ID'))
        else:
            try:
                data_id = int(data_id)
                data = self.query_set.get(id=data_id)
                data.delete()
                return JsonResponse(data=self._success_msg(data=None))
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)))

    def format_json(self, value):
        if value == 'false':
            return False
        elif value == 'true':
            return True
        else:
            return value


class RestApi(View, RestViewMixin):

    def __init__(self, *args, **kwargs):
        super(RestApi, self).__init__(*args, **kwargs)

