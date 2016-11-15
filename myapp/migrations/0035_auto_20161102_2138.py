# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0034_auto_20161102_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='oper_log',
            name='sqltype',
            field=models.CharField(default='select', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterIndexTogether(
            name='oper_log',
            index_together=set([('dbtag', 'sqltype', 'create_time')]),
        ),
    ]
