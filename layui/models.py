#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
import ast


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)  # use str(value) in Python 3


class DictField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python Dict"

    def __init__(self, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, dict):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)  # use str(value) in Python 3
