# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0035_auto_20161102_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='export_limit',
            field=models.IntegerField(default=200),
        ),
    ]
