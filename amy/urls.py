#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from views import LoginView, IndexView, MenusApi
from views import UserRestApi, AddSubMenuView


urlpatterns = [
    url(r'^login/', view=LoginView.as_view(), name='login'),
    url(r'^logout/', view='amy.views.logout', name='logout'),
    url(r'^', include(MenusApi.urls())),
    url(r'^$', view=IndexView.as_view(), name='index'),
    url(r'^', include(UserRestApi.urls())),
    url(r'^amy/menus/sub/create/(.+)/$', view=AddSubMenuView.as_view(), name='add_sub_menus'),
]
