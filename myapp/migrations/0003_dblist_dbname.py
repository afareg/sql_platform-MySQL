# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_dblist'),
    ]

    operations = [
        migrations.AddField(
            model_name='dblist',
            name='dbname',
            field=models.CharField(default='dbname', max_length=30),
            preserve_default=False,
        ),
    ]
