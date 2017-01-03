#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect, QueryDict
from django.views.generic import TemplateView
from forms import CreateUserForm, CreateMenuForm, SubMenuForm
from layui.views import RestApi, LayUiFromView
from models import Menus
from action import ChangePassAction, EnableUserAction, AddSubMenuAction


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


class MenusApi(RestApi):
    models = Menus
    form_class = CreateMenuForm
    name = u'菜单'
    form_name = u'创建菜单'
    action = [AddSubMenuAction]

    @property
    def _get_menus(self):
        return [model_to_dict(data) for data in Menus.objects.all()] + self.default_menus

    @property
    def default_menus(self):
        return [
            {
                "title": u"Docker",
                "icon": "fa-cubes",
                "spread": False,
                "children": [
                    {
                        "title": u"主机",
                        "icon": "fa-desktop",
                        "href": "/docker_ui/dockerhost/"
                    },
                    {
                        "title": u"模板配置",
                        "icon": "fa-tags",
                        "href": "/docker_ui/dockertemplate/"
                    },
                    {
                        "title": u"日志配置",
                        "icon": "fa-cogs",
                        "href": "/docker_ui/logserver/"
                    },
                    {
                        "title": u"镜像",
                        "icon": "fa-cogs",
                        "href": "/docker_ui/dockerimages/"
                    },
                    {
                        "title": u"仓库",
                        "icon": "fa-building",
                        "href": "/docker_ui/registry/"
                    }
                ]
            },
            {
                "title": u"站点设置",
                "icon": "fa-cogs",
                "spread": False,
                "children": [
                    {
                        "title": u"用户设置",
                        "icon": "fa-user-o",
                        "href": "/auth/user/"
                    },
                    {
                        "title": u"菜单配置",
                        "icon": "fa-navicon",
                        "href": "/amy/menus"
                    }
                ]
            },

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


class AddSubMenuView(LayUiFromView):
    form_class = SubMenuForm
    api_url = '/api/amy/menus/{}/'
    form_name = u'添加子菜单'

    def get(self, request, *args, **kwargs):
        menu_id = args[0]
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form, api_url=self.api_url.format(menu_id)))


class UserRestApi(RestApi):
    models = User
    form_class = CreateUserForm
    form_name = u'创建用户'
    name = u'用户'
    list_display = ('id', 'username', 'email', 'is_active', 'last_login')
    action = [ChangePassAction, EnableUserAction]

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
