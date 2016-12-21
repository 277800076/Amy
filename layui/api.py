#! /usr/bin/env python
# coding=utf-8
from django.db.models import Model
from amy.models import Menus
from django.views.generic import View
from django.http import JsonResponse, QueryDict
from django.forms import model_to_dict
from django.conf.urls import include, url, patterns




