# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import layui.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64, verbose_name='\u83dc\u5355\u540d')),
                ('icon', models.CharField(default='fa-task', max_length=64, verbose_name='\u56fe\u6807')),
                ('spread', models.BooleanField(default=True, verbose_name='\u5c55\u5f00')),
                ('children', layui.models.ListField(verbose_name='\u5b50\u83dc\u5355')),
            ],
            options={
                'db_table': 'cfg_menus',
                'verbose_name': '',
                'verbose_name_plural': '',
            },
        ),
    ]
