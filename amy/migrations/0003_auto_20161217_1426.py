# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import layui.models


class Migration(migrations.Migration):

    dependencies = [
        ('amy', '0002_auto_20161217_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menus',
            name='children',
            field=layui.models.ListField(default=[], verbose_name='\u5b50\u83dc\u5355'),
        ),
    ]
