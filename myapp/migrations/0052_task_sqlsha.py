# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0051_auto_20161110_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='sqlsha',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
