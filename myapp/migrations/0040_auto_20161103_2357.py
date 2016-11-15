# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_auto_20161103_2335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_profile',
            options={'permissions': (('can_mysql_query', 'can see mysql_query view'), ('can_log_query', 'can see log_query view'), ('can_export', 'can export csv'), ('can_insert_mysql', 'can see insert mysql'), ('can_update_mysql', 'can see update mysql'), ('can_delete_mysql', 'can see delete mysql'), ('can_create_mysql', 'can see create mysql'), ('can_drop_mysql', 'can see drop mysql'), ('can_truncate_mysql', 'can see truncate mysql'), ('can_alter_mysql', 'can see alter mysql'))},
        ),
    ]
