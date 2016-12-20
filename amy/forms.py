#! /usr/bin/env python
# coding=utf-8
from layui.widgets import StringFiled, PasswordField, EmailFiled
from django.forms import BooleanField
from django.forms import Form


class CreateUserForm(Form):
    username = StringFiled(label=u'用户名')
    password = PasswordField(label=u'密码')
    email = EmailFiled(label=u'邮箱')


class CreateMenuForm(Form):
    title = StringFiled(label=u'标题')
    icon = StringFiled(label=u'图标')
    spread = BooleanField(label=u'展开')


class SubMenuForm(Form):
    title = StringFiled(required=True, label=u'标题')
    icon = StringFiled(required=True, label=u'图标')
    href = StringFiled(required=True, label=u'链接')
