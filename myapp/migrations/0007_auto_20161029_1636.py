# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20161029_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_account',
            name='dbname',
        ),
        migrations.RemoveField(
            model_name='db_name',
            name='instance',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Db_account',
        ),
        migrations.DeleteModel(
            name='Db_instance',
        ),
        migrations.DeleteModel(
            name='Db_name',
        ),
    ]
