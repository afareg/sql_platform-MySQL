# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20161029_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_account',
            name='dbname',
        ),
        migrations.AddField(
            model_name='db_account',
            name='dbname',
            field=models.ManyToManyField(to='myapp.Db_name'),
        ),
    ]
