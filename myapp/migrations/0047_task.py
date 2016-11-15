# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0046_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=35)),
                ('ipaddr', models.CharField(max_length=35)),
                ('dbtag', models.CharField(max_length=35)),
                ('sqltext', models.TextField()),
                ('create_time', models.DateTimeField(db_index=True)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]
