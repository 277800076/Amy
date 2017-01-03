#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import Form
from layui.widgets import RequiredStringField, StringField, ChoiceField, NumberField
from django.forms import ModelChoiceField
from models import LogServer, DockerImages, Registry, DockerTemplateOption

option = (
    ('environment', '-e'),
    ('port_bindings', '-p'),
    ('binds', '-v'),
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
    version = StringField(label=u'版本')
    template = ModelChoiceField(queryset=DockerTemplateOption.objects.all(), label=u'模版')
    log_server = ModelChoiceField(queryset=LogServer.objects.all(), label=u'日志服务')
    custom = StringField(label=u'自定义')


class ContainerTemplateForm(Form):
    name = RequiredStringField(label=u'模版名称')
    images = ModelChoiceField(queryset=DockerImages.objects.all(), label=u'镜像')


class ImageFrom(Form):
    images = RequiredStringField(label=u'镜像名称')
    registry = ModelChoiceField(queryset=Registry.objects.all(), label=u'仓库')


class OptionForm(Form):
    key = ChoiceField(choices=option, label=u'配置')
    value = StringField(label=u'参数')


class DockerHostAddForm(Form):
    address = RequiredStringField(label=u'地址')
    port = NumberField(label=u'端口')
    tag = RequiredStringField(label=u'类型')


class DockerTemplateForm(Form):
    images = ModelChoiceField(queryset=DockerImages.objects.all(), label=u'镜像')


class DockerTemplateOptionForm(Form):
    # template = ModelChoiceField(queryset=DockerTemplate.objects.all())
    option = ChoiceField(choices=option, label=u'配置名')
    key = StringField(label=u'参数')
    value = StringField(label=u'值')
