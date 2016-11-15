# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_user_profile_export_limit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_profile',
            options={'permissions': (('can_mysql_query', 'can see mysql_query view'), ('can_log_query', 'can see log_query view'), ('can_export', 'can export csv'))},
        ),
    ]
