#! /usr/bin/env python
# coding=utf-8
from layui.widgets import StringField, PasswordField, EmailField
from django.forms import BooleanField
from django.forms import Form


class CreateUserForm(Form):
    username = StringField(label=u'用户名')
    password = PasswordField(label=u'密码')
    email = EmailField(label=u'邮箱')


class CreateMenuForm(Form):
    title = StringField(label=u'标题')
    icon = StringField(label=u'图标')
    spread = BooleanField(label=u'展开')


class SubMenuForm(Form):
    title = StringField(required=True, label=u'标题')
    icon = StringField(required=True, label=u'图标')
    href = StringField(required=True, label=u'链接')
