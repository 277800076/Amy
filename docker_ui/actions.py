#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import your module
from layui.actions import BtnShow, JSAction


class TemplateOptionAction(JSAction):
    name = u'添加参数'
    icon = u'fa fa-plus'
    action_type = 'show'
    action_url = '/docker_ui/dockertemplateoption/create/{}'

    def __html__(self):
        _html = u'''<a href="javascript:;" onclick="{js}('{title}', '{url}')" title={title}>{icon}</a>&nbsp;'''
        return _html.format(url=self.action_url.format(self.obj.id), js=self._js, icon=self._get_icon, title=self.name)


class TemplateOptionShow(JSAction):
    name = u'查看参数'
    icon = u'fa fa-tasks'
    action_type = 'show'
    action_url = '/docker_ui/dockertemplateoption/{}'

    def __html__(self):
        _html = u'''<a href="javascript:;" onclick="{js}('{title}', '{url}')" title={title}>{icon}</a>&nbsp;'''
        return _html.format(url=self.action_url.format(self.obj.id), js=self._js, icon=self._get_icon, title=self.name)


class DockerContainerShow(JSAction):
    name = u'查看容器'
    icon = u'fa fa-tasks'
    action_type = 'show'
    action_url = '/docker_ui/docker/{}'

    def __html__(self):
        _html = u'''<a href="javascript:;" onclick="{js}('{title}', '{url}')" title={title}>{icon}</a>&nbsp;'''
        return _html.format(url=self.action_url.format(self.obj.id), js=self._js, icon=self._get_icon, title=self.name)
