#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class Registry(models.Model):
    registry = models.CharField(max_length=64, verbose_name=u'仓库名')
    username = models.CharField(max_length=64, verbose_name=u'用户名')
    password = models.CharField(max_length=64, verbose_name=u'密码')

    def __unicode__(self):
        return self.registry

    class Meta:
        db_table = 'docker_registry'


class LogServer(models.Model):
    address = models.CharField(max_length=15, verbose_name=u'地址')
    port = models.CharField(max_length=5, verbose_name=u'端口')
    tag = models.CharField(max_length=16, verbose_name=u'标签')

    def __unicode__(self):
        return "%s:%s-%s" % (self.address, self.port, self.tag)

    class Meta:
        db_table = 'docker_log_option'


class DockerContainerTemplate(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'容器名')
    images = models.CharField(max_length=32, verbose_name=u'镜像名')
    log_server = models.ForeignKey(LogServer, null=True, verbose_name=u'日志服务器')
    registry = models.ForeignKey(Registry, null=True, verbose_name=u'镜像仓库')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'docker_container_template'


class DockerContainerOption(models.Model):
    key = models.CharField(max_length=32, null=False, verbose_name=u'键')
    value = models.CharField(max_length=64, null=False, verbose_name=u'值')
    container = models.ForeignKey(DockerContainerTemplate, verbose_name=u'容器')

    def __unicode__(self):
        return '%s=%s' % (self.key, self.value)

    class Meta:
        db_table = 'docker_container_option'
