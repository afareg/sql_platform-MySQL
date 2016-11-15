# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_my_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='my_user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='my_user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='My_user',
        ),
    ]
