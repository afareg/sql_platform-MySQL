# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_delete_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_instance',
            name='role',
            field=models.CharField(default='read', max_length=30),
            preserve_default=False,
        ),
    ]
