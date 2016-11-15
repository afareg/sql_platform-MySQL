# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20161029_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='db_account',
            old_name='read_write',
            new_name='role',
        ),
        migrations.AddField(
            model_name='db_instance',
            name='port',
            field=models.CharField(default='1', max_length=10),
            preserve_default=False,
        ),
    ]
