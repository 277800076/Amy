#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from layui.models import DictField, ListField


# Create your models here.
class Menus(models.Model):
    title = models.CharField(max_length=64, verbose_name=u'菜单名')
    icon = models.CharField(max_length=64, default=u'fa-task', verbose_name=u'图标')
    spread = models.BooleanField(default=True, verbose_name=u'展开')
    children = ListField(default=[], verbose_name=u'子菜单')

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'cfg_menus'
        verbose_name = u''
        verbose_name_plural = verbose_name

