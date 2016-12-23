#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from layui.models import ListField


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

    def log_config(self):
        return {
            "Type": "gelf",
            "Config": {
                "gelf-address": "udp://%s:%s" % (self.address, self.port),
                "tag": self.tag
            }
        }

    class Meta:
        db_table = 'docker_log_option'


class DockerImages(models.Model):
    images = models.CharField(max_length=64, verbose_name=u'镜像名称')
    registry = models.ForeignKey(Registry, null=True, verbose_name=u'镜像仓库')

    def __unicode__(self):
        return self.images

    class Meta:
        db_table = 'docker_images'


class DockerHost(models.Model):
    address = models.CharField(max_length=64, verbose_name=u'地址')
    port = models.IntegerField(verbose_name=u'端口')
    tag = models.CharField(max_length=64, verbose_name=u'类型')

    def __unicode__(self):
        return "%s-%s" % (self.tag, self.address)

    @property
    def base_url(self):
        return 'tcp://{host}:{port}'.format(host=self.host, port=self.port)

    class Meta:
        db_table = 'docker_host_config'


class DockerTemplateOption(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'容器名')
    binds = ListField(verbose_name=u'目录映射')
    port_bindings = ListField(verbose_name=u'端口映射')
    publish_all_ports = models.BooleanField(default=False, verbose_name=u'端口随机')
    privileged = models.BooleanField(default=True, verbose_name=u'超级权限')
    network_mode = models.BooleanField(default=False, verbose_name=u'host模式')
    extra_hosts = ListField(verbose_name=u'主机映射')
    environment = ListField(verbose_name=u'环境变量')
    command = models.CharField(max_length=64, verbose_name=u'命令')
    images = models.ForeignKey(DockerImages, verbose_name=u'镜像')

    def __unicode__(self):
        return '%s-option' % self.template

    class Meta:
        db_table = 'docker_container_option'
