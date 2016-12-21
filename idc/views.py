#!/usr/bin/env python
# -*- coding: utf-8 -*-
from layui.views import RestApi
from django.contrib.auth.models import User
from amy.forms import CreateUserForm


# Create your views here.
class TestRestApi(RestApi):
    models = User
    form_class = CreateUserForm
    form_name = u'创建用户'
    name = u'用户'
    exclude_field = ('password', 'is_superuser')
