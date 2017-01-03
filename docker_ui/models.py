#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from layui.models import ListField
from addict import Dict
from docker.utils.types import LogConfig
from hashers.docker.client import Docker


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
        return LogConfig(**{
            "Type": "gelf",
            "Config": {
                "gelf-address": "udp://%s:%s" % (self.address, self.port),
                "tag": self.tag
            }
        })

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
    def docker_cli(self):
        return Docker(base_url='tcp://{host}:{port}'.format(host=self.address, port=self.port))

    class Meta:
        db_table = 'docker_host_config'


class DockerTemplate(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=u'容器名')
    publish_all_ports = models.BooleanField(default=False, verbose_name=u'端口随机')
    privileged = models.BooleanField(default=True, verbose_name=u'超级权限')
    network_mode = models.BooleanField(default=False, verbose_name=u'host模式')
    command = models.CharField(max_length=128, verbose_name=u'命令')
    images = models.ForeignKey(DockerImages, verbose_name=u'镜像')

    def __unicode__(self):
        return self.name

    def config(self):
        return {
            'publish_all_ports': self.publish_all_ports,
            'privileged': self.privileged,
            'network_mode': 'host' if self.network_mode else 'default',
            'command': self.command if self.command else None
        }

    def registry(self):
        return self.images.registry

    def image(self):
        return self.images.images

    class Meta:
        db_table = 'docker_template'


class DockerTemplateOption(models.Model):
    template = models.ForeignKey(DockerTemplate, verbose_name=u'模板名')
    option = models.CharField(max_length=32, verbose_name=u'配置名')
    key = models.CharField(max_length=32, verbose_name=u'参数')
    value = models.CharField(max_length=32, verbose_name=u'值')

    def __unicode__(self):
        return '%s:%s=%s' % (self.option, self.key, self.value)

    class Meta:
        db_table = 'docker_template_option'

DockerContainerModels = Dict({
    '_meta': {
        'model_name': 'docker',
        'app_label': 'docker_ui',
        'local_fields': [
            {'name': u'Status', 'verbose_name': u'启动时间', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'Created', 'verbose_name': u'创建时间', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'Image', 'verbose_name': u'镜像', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'Labels', 'verbose_name': u'标签', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'NetworkSettings', 'verbose_name': u'网络', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'HostConfig', 'verbose_name': u'配置', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'ImageID', 'verbose_name': u'镜像ID', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'State', 'verbose_name': u'状态', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'Command', 'verbose_name': u'命令', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'Names', 'verbose_name': u'容器名称', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'Mounts', 'verbose_name': u'卷组', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'Id', 'verbose_name': u'容器ID', 'model_name': 'docker', 'app_label': 'docker_ui'},
            {'name': u'Ports', 'verbose_name': u'端口', 'model_name': 'docker', 'app_label': 'docker_ui'}
        ]
    }
})
