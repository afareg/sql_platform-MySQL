# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_dblist_dbname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Db_account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dbname', models.CharField(max_length=30)),
                ('user', models.CharField(max_length=30)),
                ('passwd', models.CharField(max_length=30)),
                ('read_write', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Db_instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Db_name',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dbtag', models.CharField(max_length=30)),
                ('dbname', models.CharField(max_length=30)),
                ('instance', models.ForeignKey(to='myapp.Db_instance')),
            ],
        ),
        migrations.DeleteModel(
            name='Dblist',
        ),
        migrations.AddField(
            model_name='db_account',
            name='dbtag',
            field=models.ForeignKey(to='myapp.Db_name'),
        ),
    ]
