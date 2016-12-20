#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from views import LoginView, IndexView, MenuView, UserList, CreateUserFormView, MenusApi, CreateMenuFormView, SubMenuFormView
from views import UserRestApi


urlpatterns = [
    url(r'^login/', view=LoginView.as_view(), name='login'),
    url(r'^logout/', view='amy.views.logout', name='logout'),
    url(r'^menus/$', view=MenuView.as_view(), name='menus'),
    url(r'^menus/create/', view=CreateMenuFormView.as_view(), name='create_menus'),
    url(r'^menus/sub/create/(.+)/$', view=SubMenuFormView.as_view(), name='create_sub_menus'),
    url(r'^', include(MenusApi.urls())),
    url(r'^$', view=IndexView.as_view(), name='index'),
    url(r'^user/$', view=UserList.as_view(), name='user'),
    url(r'^user/create/', view=CreateUserFormView.as_view(), name='create_user'),
    url(r'^', include(UserRestApi.urls())),
]
