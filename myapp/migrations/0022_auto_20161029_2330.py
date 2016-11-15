# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_db_instance_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_instance',
            name='role',
            field=models.CharField(default='read', max_length=30, choices=[('read', 'read'), ('write', 'write')]),
        ),
    ]
