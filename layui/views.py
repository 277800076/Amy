# coding=utf-8
from django.http import JsonResponse, QueryDict
from django.conf.urls import include, url, patterns
from addict import Dict
from django.views.generic import FormView, View
from django.shortcuts import render_to_response
import datetime
from actions import BtnShow, JSAction
from django.db.models import ForeignKey
from models import ListField, DictField


class LayUiBaseViews(object):
    models = None
    name = u''

    @staticmethod
    def _success_msg(data):
        return {'result': 'success', 'data': data}

    @staticmethod
    def _failure_msg(code):
        return {'result': 'failure', 'code': code}

    def get_name(self):
        if self.name:
            return self.name
        else:
            return None

    def get_queryset(self, request, *args, **kwargs):
        return self.models.objects.all()

    @staticmethod
    def format_json(value):
        if value == 'false':
            return False
        elif value == 'true':
            return True
        elif value == 'on':
            return True
        else:
            return value

    def get_api_url(self, request, *args, **kwargs):
        return r'/api/%s/%s/' % (self.models._meta.app_label, self.models._meta.model_name)

    def table(self, request, *args, **kwargs):
        pass

    def form(self, request, *args, **kwargs):
        pass

    def rest_api(self):
        pass


class LayUIFormMixin(LayUiBaseViews):
    form_template = 'form.html'
    form_class = None
    form_name = u''

    @classmethod
    def form(cls, request, *args, **kwargs):
        context = {
            'form': cls.form_class(),
            'view': cls,
            'api_url': cls().get_api_url(request, *args, **kwargs)
        }
        return render_to_response(template_name=cls.form_template, context=context)


class RestViewMixin(LayUiBaseViews):
    exclude_field = ()

    @property
    def query_set(self):
        return self.models.objects.all()

    @property
    def _list_display(self):
        return [field.name for field in self.models._meta.local_fields if field.name not in self.exclude_field]

    def get_foreign(self, field, value):
        _f = field.related_model()
        models = _f._meta.model
        return models.objects.get(pk=int(value))

    def save(self, request):
        _post = request.POST.dict()
        foreign = [field for field in self.models._meta.local_fields if type(field) == ForeignKey]
        for _field in foreign:
            if _field.name in _post:
                _f = _post[_field.name]
                if _f:
                    _post[_field.name] = self.get_foreign(_field, _f)
                else:
                    del _post[_field.name]
        list_field = [field for field in self.models._meta.local_fields if type(field) == ListField]
        return _post, {_field.name: _post.pop(_field.name)for _field in list_field if _field.name in _post}

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
        _data, _list_field = self.save(request)
        try:
            post = {v: self.format_json(_data[v]) for v in _data}
            data = self.models(**post)
            if _list_field:
                for _field in _list_field:
                    field = getattr(data, _field)
                    field.append(_list_field[_field])
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


class LayUiTableMixin(LayUiBaseViews):
    table_template = 'table.html'
    order = ''
    exclude_field = ()
    action = []
    btn = []
    list_display = ()

    def _get_td(self, request, *args, **kwargs):
        _html = u''
        for obj in self.get_queryset(request, *args, **kwargs):
            _td = ''.join([self._format_value(obj, _field)
                           for _field in self._get_list_display if hasattr(obj, _field)])

            actions = [act(request, obj) for act in self.action]
            actions.append(JSAction(request, obj, **{'action_type': 'delete', 'icon': 'fa fa-trash'}))

            _td += u'<td>{}</td>'.format(''.join([act.__html__() for act in actions]))
            _html += u'<tr>{}</tr>'.format(_td)
        return _html

    def _format_value(self, data, _field):
        value = getattr(data, _field)
        if type(value) == bool:
            if value:
                return u'<td><i class="fa fa-check"></i></td>'
            else:
                return u'<td><i class="fa fa-remove"></i></td>'
        elif type(value) == datetime.datetime:
            return u'<td>{}</td>'.format(value.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            return u'<td>{}</td>'.format(value)

    @property
    def _get_list_display(self):
        if self.list_display:
            return [field for field in self.list_display if field not in self.exclude_field]
        else:
            return [field.name for field in self.models._meta.local_fields if field.name not in self.exclude_field]

    def _table_th(self):
        list_display = self._get_list_display
        _model_fields = self.models._meta.local_fields
        _all_field = [field.name for field in _model_fields]
        _last_filed = [_model_fields[_all_field.index(field)].verbose_name
                       for field in list_display if field in _all_field]
        return _last_filed + [u'操作']

    def _get_order(self):
        if self.order:
            return self._get_list_display.index(self.order)
        else:
            return 0

    def _get_btn(self, *args, **kwargs):
        _btn = [{
            'open_url': '/%s/%s/create/' % (self.models._meta.app_label, self.models._meta.model_name),
            'name': u'添加' + self.get_name(),
        }]

        self.btn = self.btn + _btn
        return [BtnShow(**data).__html__() for data in self.btn]

    def get_context_data(self, request, *args, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['object_list'] = self.get_queryset(request)
        kwargs['table_td'] = self._get_td(request)
        kwargs['table_th'] = self._table_th()
        kwargs['order'] = self._get_order()
        kwargs['btns'] = self._get_btn(*args, **kwargs)
        return kwargs

    @classmethod
    def table(cls, request, *args, **kwargs):
        context = cls().get_context_data(request, *args, **kwargs)
        return render_to_response(template_name=cls.table_template, context=context)


class RestApi(View,
              RestViewMixin,
              LayUIFormMixin,
              LayUiTableMixin):

    @classmethod
    def urls(cls):
        urlpatterns = patterns(
            '',
            url(r'api/%s/%s/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.as_view(),
                name=cls.__name__),
            url(r'api/%s/%s/(.+)/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.as_view(),
                name=cls.__name__),
            url(r'%s/%s/create/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.form,
                name=cls.__name__),
            url(r'%s/%s/$' % (cls.models._meta.app_label, cls.models._meta.model_name), view=cls.table,
                name=cls.__name__)
        )
        return urlpatterns


class LayUiFromView(FormView, LayUIFormMixin):
    template_name = 'form.html'
    api_url = ''

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))





