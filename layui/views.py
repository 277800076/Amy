# coding=utf-8
from django.http import JsonResponse
from django.views.generic import FormView, TemplateView
import datetime


class LayUiFormViews(FormView):
    template_name = 'form.html'
    form_name = u''
    ajax_url = ''

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'Error', 'message': form.errors.as_text()})


class LayUiTableViews(TemplateView):
    model = None
    template_name = 'table.html'
    list_display = ()
    order = ''
    exclude_field = ()
    name = u''
    action = []
    btn = []

    def get_queryset(self):
        return self.model.objects.all()

    def _get_td(self):
        _html = u''
        for data in self.get_queryset():
            _td = ''.join([self._format_value(data, _field)
                           for _field in self._get_list_display if hasattr(data, _field)])
            if self.action:
                _td += u'<td>{}</td>'.format(''.join([act(self.request, data).__html__() for act in self.action]))
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
            return [field.name for field in self.model._meta.local_fields if field.name not in self.exclude_field]

    def _table_th(self):
        list_display = self._get_list_display
        _model_fields = self.model._meta.local_fields
        _all_field = [field.name for field in _model_fields]
        _last_filed = [_model_fields[_all_field.index(field)].verbose_name
                       for field in list_display if field in _all_field]
        return _last_filed + [u'操作'] if self.action else _last_filed

    def _get_order(self):
        if self.order:
            return self._get_list_display.index(self.order)
        else:
            return 0

    def _get_btn(self):
        if self.btn:
            return [data().__html__() for data in self.btn]
        else:
            return None

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['table_th'] = self._table_th()
        kwargs['object_list'] = self.get_queryset()
        kwargs['table_td'] = self._get_td()
        kwargs['order'] = self._get_order()
        kwargs['btns'] = self._get_btn()
        return kwargs
