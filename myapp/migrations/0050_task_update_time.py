# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0049_auto_20161108_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 7, 16, 35, 43, 763000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
