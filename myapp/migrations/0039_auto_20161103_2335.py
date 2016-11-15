# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0038_auto_20161103_2334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_profile',
            options={'permissions': (('can_mysql_query', 'can see mysql_query view'), ('can_log_query', 'can see log_query view'), ('can_export', 'can export csv'), ('can_insert_mysql', 'can see insert mysql'), ('can_update_mysql', 'can see update mysql'), ('can_delete_mysql', 'can see delete mysql'))},
        ),
    ]
