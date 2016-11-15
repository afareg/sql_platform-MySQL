# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_auto_20161029_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_name',
            name='account',
        ),
    ]
