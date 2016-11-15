# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_auto_20161101_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='oper_log',
            name='dbtag',
            field=models.CharField(default='mysql-lepus', max_length=35),
            preserve_default=False,
        ),
    ]
