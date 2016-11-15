# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_oper_log_dbtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_name',
            name='dbtag',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
