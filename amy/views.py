#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect, QueryDict
from django.views.generic import TemplateView

from action import AddSubMenuAction
from action import DeleteAction, ChangePassAction, EnableUserAction, DeleteMenuAction
from forms import CreateUserForm, CreateMenuForm, SubMenuForm
from layui.views import RestApi
from layui.views import LayUiTableViews, LayUiFormViews
from models import Menus


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'failure'})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')


class IndexView(TemplateView):
    template_name = 'index.html'
    footer = u'Amy Operation(Mu77)'
    site = u'Amy Operation'


class MenuView(LayUiTableViews):
    model = Menus
    name = u'菜单列表'
    exclude_field = ('children',)
    action = [DeleteMenuAction, AddSubMenuAction]
    btn = [{'open_url': '/menus/create/', 'name': u'添加菜单'}]


class CreateMenuFormView(LayUiFormViews):
    form_class = CreateMenuForm
    form_name = u'创建菜单'
    ajax_url = '/api/menus/'


class MenusApi(RestApi):
    models = Menus

    @property
    def _get_menus(self):
        return [model_to_dict(data) for data in Menus.objects.all()] + self.default_menus

    @property
    def default_menus(self):
        return [
            {
                "title": u"站点设置",
                "icon": "fa-cogs",
                "spread": False,
                "children": [
                    {
                        "title": u"用户设置",
                        "icon": "fa-user-o",
                        "href": "/user"
                    },
                    {
                        "title": u"权限设置",
                        "icon": "fa-lock",
                        "href": "/auth"
                    },
                    {
                        "title": u"菜单配置",
                        "icon": "fa-navicon",
                        "href": "/menus"
                    }
                ]
            }
        ]

    def get(self, request, data_id=None, *args, **kwargs):
        if data_id is None:
            try:
                data = self._get_menus
                return JsonResponse(data, safe=False)
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)), safe=False)
        else:
            try:
                data_id = int(data_id)
                data = [self.models.objects.values(*self._list_display).get(id=data_id)]
                return JsonResponse(data=data, safe=False)
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)), safe=False)

    def post(self, request, data_id=None, *args, **kwargs):
        if data_id is None:
            try:
                post = {v: self.format_json(request.POST.dict()[v]) for v in request.POST.dict()}
                data = self.models(**post)
                data.save()
                return JsonResponse(data=self._success_msg(None), safe=False)
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)))
        else:
            try:
                data_id = int(data_id)
                data = self.query_set.get(pk=data_id)
                data.children.append(request.POST.dict())
                data.save()
                return JsonResponse(data=self._success_msg(None), safe=False)
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)))


class UserList(LayUiTableViews):
    model = User
    list_display = ('id', 'username', 'email', 'is_active', 'is_superuser', 'last_login')
    exclude_field = ('password',)
    name = u'用户列表'
    action = [DeleteAction, ChangePassAction, EnableUserAction]
    btn = [{'open_url': '/user/create/', 'name': u'添加用户'}]


class CreateUserFormView(LayUiFormViews):
    form_class = CreateUserForm
    form_name = u'创建用户'
    ajax_url = '/api/user/'


class SubMenuFormView(LayUiFormViews):
    form_class = SubMenuForm
    form_name = u'创建子菜单'
    ajax_url = '/api/menus/{}/'

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        self.ajax_url = self.ajax_url.format(args[0])
        return self.render_to_response(self.get_context_data(form=form))


class UserRestApi(RestApi):
    models = User
    exclude_field = ('password',)

    def post(self, request, data_id=None, *args, **kwargs):
        try:
            post_data = request.POST.dict()
            self.models.objects.create_user(**post_data)
            return JsonResponse(data=self._success_msg(data=None))
        except Exception, e:
            return JsonResponse(data=self._failure_msg(str(e)))

    def put(self, request, data_id=None, *args, **kwargs):
        if data_id is None:
            return JsonResponse(data=self._failure_msg(u'No specified data ID'))
        else:
            try:
                data_id = int(data_id)
                put = QueryDict(request.body, encoding=request.encoding)
                password = put.get('password', None)
                if password is None:
                    data = self.models.objects.filter(pk=data_id)
                    data.update(**{v: self.format_json(put.dict()[v]) for v in put.dict()})
                    data = data[0]
                else:
                    data = self.query_set.get(id=data_id)
                    data.set_password(put.get('password'))
                data.save()
                return JsonResponse(data=self._success_msg(data=None))
            except Exception, e:
                return JsonResponse(data=self._failure_msg(str(e)))
