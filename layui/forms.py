#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import Form
from widgets import StringFiled, EmailFiled, PhoneFiled, NumberField, IdentityFiled, DateField, RadioField
from django import forms
from django.forms.fields import BooleanField


# create coding
class LayUiForm(forms.Form):
    name = StringFiled(label=u'测试', max_length=12, min_length=3)
    select = forms.ChoiceField(label=u'测试2', choices=((1, 0), (2, 3)))
    radio = RadioField(label=u'测试Radio', choices=((1, u'BOY'), (2, 'GIRL')))
    email = EmailFiled(label=u'邮箱')
    phone = PhoneFiled(label=u'手机')
    create_at = DateField(label=u'创建时间')
    identity = IdentityFiled(label=u'身份证')
    boolf = BooleanField(label=u'sss')
