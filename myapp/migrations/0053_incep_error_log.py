# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0052_task_sqlsha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incep_error_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('myid', models.IntegerField()),
                ('stage', models.CharField(max_length=20)),
                ('errlevel', models.IntegerField()),
                ('stagestatus', models.CharField(max_length=40)),
                ('errormessage', models.TextField()),
                ('sqltext', models.TextField()),
                ('affectrow', models.IntegerField()),
                ('sequence', models.CharField(max_length=30)),
                ('backup_db', models.CharField(max_length=100)),
                ('execute_time', models.CharField(max_length=20)),
                ('sqlsha', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField(db_index=True)),
                ('finish_time', models.DateTimeField()),
            ],
        ),
    ]
