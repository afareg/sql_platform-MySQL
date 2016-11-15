# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20161029_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_name',
            name='instance',
        ),
        migrations.AddField(
            model_name='db_name',
            name='instance',
            field=models.ManyToManyField(to='myapp.Db_instance'),
        ),
    ]
