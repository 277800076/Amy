#! /usr/bin/env python
# coding=utf-8
from layui.actions import JSAction, BtnShow


class ChangePassAction(JSAction):
    name = u'修改密码'
    icon = u'fa fa-lock'
    action_type = 'change_pass'


class EnableUserAction(JSAction):
    name = u'启用'
    icon = u'fa fa-arrow-up'
    action_type = 'change_pass'

    @property
    def _get_icon(self):
        if self.obj.is_active:
            return u'<i class="fa fa-arrow-down"></i>'
        else:
            return u'<i class="fa fa-arrow-up"></i>'

    @property
    def _js(self):
        if self.obj.is_active:
            return u"disable_user"
        else:
            return u'enable_user'

    @property
    def _title(self):
        if self.obj.is_active:
            return u"禁用"
        else:
            return u'启用'

    def __html__(self):
        _html = u'''<a href="javascript:;" onclick="{js}(this, '{url}')" title={title}>{icon}</a>&nbsp;'''
        return _html.format(url=self._action_url, js=self._js, icon=self._get_icon, title=self._title)


class AddSubMenuAction(JSAction):
    name = u'添加子菜单'
    icon = u'fa fa-plus'
    action_type = 'show'
    action_url = '/amy/menus/sub/create/{}'

    def __html__(self):
        _html = u'''<a href="javascript:;" onclick="{js}('{title}', '{url}')" title={title}>{icon}</a>&nbsp;'''
        return _html.format(url=self.action_url.format(self.obj.id), js=self._js, icon=self._get_icon, title=self.name)
