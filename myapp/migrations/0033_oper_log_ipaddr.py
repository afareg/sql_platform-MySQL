# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_auto_20161102_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='oper_log',
            name='ipaddr',
            field=models.CharField(default='127.0.0.1', max_length=35),
            preserve_default=False,
        ),
    ]
