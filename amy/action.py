#! /usr/bin/env python
# coding=utf-8
from layui.actions import JSAction, BtnShow


class DeleteAction(JSAction):
    name = u'删除'
    icon = u'fa fa-trash'
    action_url = '/api/user'
    action_type = 'delete'


class DeleteMenuAction(JSAction):
    name = u'删除'
    icon = u'fa fa-trash'
    action_url = '/api/menus'
    action_type = 'delete'


class ChangePassAction(JSAction):
    name = u'修改密码'
    icon = u'fa fa-lock'
    action_url = '/api/user'
    action_type = 'change_pass'


class EnableUserAction(JSAction):
    name = u'启用'
    icon = u'fa fa-arrow-up'
    action_url = '/api/user'
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
    action_url = '/menus/sub/create'
    action_type = 'show'

    def __html__(self):
        _html = u'''<a href="javascript:;" onclick="{js}('{title}', '{url}')" title={title}>{icon}</a>&nbsp;'''
        return _html.format(url=self._action_url, js=self._js, icon=self._get_icon, title=self.name)


class AddUserBtn(BtnShow):
    open_url = '/user/create/'
    name = u'添加用户'
    icon = u'fa fa-user'


class AddMenuBtn(BtnShow):
    open_url = '/menus/create/'
    name = u'添加菜单'
    icon = u'fa fa-list'
