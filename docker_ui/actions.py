#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import your module
from layui.actions import BtnShow, JSAction


# create coding
class DeleteRegistry(JSAction):
    name = u'删除'
    icon = u'fa fa-trash'
    action_url = '/api/docker/registry/'
    action_type = 'delete'


class CreateRegistryBtn(BtnShow):
    open_url = '/docker/registry/create/'
    icon = u'fa fa-plus'
    name = u'新增仓库'


class DeleteLogServer(JSAction):
    name = u'删除'
    icon = u'fa fa-trash'
    action_url = '/api/docker/log'
    action_type = 'delete'


class CreateLogServerBtn(BtnShow):
    open_url = '/docker/log/create/'
    icon = u'fa fa-plus'
    name = u'新增日志'
