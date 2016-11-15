# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20161029_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_account',
            name='tags',
            field=models.CharField(default='lepus', max_length=30),
            preserve_default=False,
        ),
    ]
