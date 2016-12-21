#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import your module


# create coding
globals_js = {
    'delete': 'data_delete',
    'change_pass': 'change_pass',
    'show': 'form_show'
}


class BtnShow(object):
    def __init__(self, open_url, name, icon=None):
        self.open_url = open_url
        self.name = name
        self.icon = icon or u'fa fa-plus'

    def __html__(self):
        return u"""
        <a class="layui-btn btn-add btn-default" onclick="form_show('{name}', '{url}')">
                          <i class="{icon}"></i> {name}</a>
        """.format(name=self.name, icon=self.icon, url=self.open_url)


class JSAction(object):
    name = u''
    icon = u'fa fa-tasks'
    action_url = ''
    action_type = 'delete'
    description = ''
    model_perm = 'change'

    def __init__(self, request, obj, action_type=None, icon=None):
        self.obj = obj
        # assert request.user.has_perm(self.model_perm, obj)
        if action_type:
            self.action_type = action_type
        if icon:
            self.icon = icon

    @property
    def _get_icon(self):
        return u'<i class="{}"></i>'.format(self.icon)

    @property
    def _js(self):
        _js = globals_js[self.action_type]
        return u"{}".format(_js)

    @property
    def _action_url(self):
        if self.action_url:
            return self.action_url.rstrip('/') + '/' + str(self.obj.id)
        else:
            return '/api/%s/%s/%s' % (self.obj._meta.app_label, self.obj._meta.model_name, str(self.obj.id))

    def __html__(self):
        _html = u'''<a href="javascript:;" onclick="{js}(this, '{url}')" title={title}>{icon}</a>&nbsp;'''
        return _html.format(url=self._action_url, js=self._js, icon=self._get_icon, title=self.name)
