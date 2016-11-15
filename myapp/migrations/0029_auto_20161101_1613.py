# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_oper_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oper_log',
            name='create_time',
            field=models.DateTimeField(),
        ),
    ]
