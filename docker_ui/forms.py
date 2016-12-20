#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import Form
from layui.widgets import RequiredStringField, StringField, ChoiceField
from django.forms import BooleanField, ModelChoiceField
from models import LogServer, DockerContainerTemplate, DockerImages, Registry


option = (
    ('environment', '-e'),
    ('publish_all_ports', '-P'),
    ('port_bindings', '-p'),
    ('binds', '-v'),
    ('command', 'command'),
    ('network_mode', '-net'),
    ('privileged', '--privileged'),
    ('extra_hosts', '--add-host')
)


# create coding
class RegistryForm(Form):
    registry = RequiredStringField(label=u'仓库名')
    username = RequiredStringField(label=u'用户名')
    password = RequiredStringField(label=u'密码')


class LogServerForm(Form):
    address = RequiredStringField(label=u'日志地址')
    port = RequiredStringField(label=u'端口')
    tag = RequiredStringField(label=u'标签')


class CreateDockerContainerForm(Form):
    name = StringField(label=u'容器名')
    template = ModelChoiceField(queryset=DockerContainerTemplate.objects.all(), label=u'模版')
    version = StringField(label=u'版本')
    log_server = ModelChoiceField(queryset=LogServer.objects.all(), label=u'日志服务')
    custom = StringField(label=u'自定义')


class ContainerTemplateForm(Form):
    name = RequiredStringField(label=u'模版名称')
    images = ModelChoiceField(queryset=DockerImages.objects.all(), label=u'镜像')


class ImageFrom(Form):
    name = RequiredStringField(label=u'镜像名称')
    registry = ModelChoiceField(queryset=Registry.objects.all(), label=u'仓库')


class OptionForm(Form):
    key = ChoiceField(choices=option, label=u'配置')
    values = StringField(label=u'参数')