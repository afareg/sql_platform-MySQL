# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_auto_20161101_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oper_log',
            name='create_time',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterIndexTogether(
            name='oper_log',
            index_together=set([('dbtag', 'create_time')]),
        ),
    ]
