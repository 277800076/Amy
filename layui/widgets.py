#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms.fields import ChoiceField
from django.forms.widgets import TextInput, NumberInput, RadioSelect, RadioFieldRenderer, RadioChoiceInput, PasswordInput
from django.forms.fields import CharField, IntegerField
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe


class StringFiled(CharField):
    widget = TextInput(attrs={'class': 'layui-input'})


class PasswordField(CharField):
    widget = PasswordInput(attrs={'class': 'layui-input'})


class EmailFiled(CharField):
    widget = TextInput(attrs={'class': 'layui-input', 'lay-verify': 'email'})


class PhoneFiled(CharField):
    widget = TextInput(attrs={'class': 'layui-input', 'lay-verify': 'phone'})


class UrlFiled(CharField):
    widget = TextInput(attrs={'class': 'layui-input', 'lay-verify': 'url'})


class IdentityFiled(CharField):
    widget = TextInput(attrs={'class': 'layui-input', 'lay-verify': 'identity'})


class NumberField(IntegerField):
    widget = NumberInput(attrs={'class': 'layui-input', 'lay-verify': 'number'})


class DateField(CharField):
    widget = TextInput(attrs={'class': 'layui-input', 'lay-verify': 'date',
                              'placeholder': 'yyyy-mm-dd', 'onclick': 'layui.laydate({elem: this})'})


class RadioInput(RadioChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        return mark_safe(u'%s' % self.tag())

    def tag(self, attrs=None):
        attrs = attrs or self.attrs
        choice_label = conditional_escape(force_str(self.choice_label))
        final_attrs = dict(attrs, type=self.input_type, name=self.name, value=self.choice_value, title=choice_label)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return format_html('<input{} />', flatatt(final_attrs))


class LayUiRadioFieldRenderer(RadioFieldRenderer):

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield RadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]
        return RadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def render(self):
        return mark_safe(u'\n'.join([force_str(w) for w in self]))


class LayUiRadioSelect(RadioSelect):
    renderer = LayUiRadioFieldRenderer


class RadioField(ChoiceField):
    widget = LayUiRadioSelect
