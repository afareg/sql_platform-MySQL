# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20161029_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_account',
            name='dbtag',
        ),
        migrations.AlterField(
            model_name='db_account',
            name='dbname',
            field=models.ForeignKey(to='myapp.Db_name'),
        ),
    ]
