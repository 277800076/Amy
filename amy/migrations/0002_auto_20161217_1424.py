# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import layui.models


class Migration(migrations.Migration):

    dependencies = [
        ('amy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menus',
            name='children',
            field=layui.models.ListField(default={}, verbose_name='\u5b50\u83dc\u5355'),
        ),
    ]
