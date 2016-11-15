# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_auto_20161031_2256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_profile',
            options={'permissions': (('mysql_query', 'can see mysql_query view'),)},
        ),
    ]
