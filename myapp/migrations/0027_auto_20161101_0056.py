# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_auto_20161101_0044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_profile',
            options={'permissions': (('can_mysql_query', 'can see mysql_query view'),)},
        ),
    ]
