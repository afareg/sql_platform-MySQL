# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0017_remove_db_name_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_account',
            name='account',
        ),
        migrations.AddField(
            model_name='db_name',
            name='account',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
