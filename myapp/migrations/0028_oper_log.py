# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_auto_20161101_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oper_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=35)),
                ('dbname', models.CharField(max_length=40)),
                ('sqltext', models.TextField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('login_time', models.DateTimeField()),
            ],
        ),
    ]
