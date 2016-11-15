# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20161029_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Db_account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=30)),
                ('passwd', models.CharField(max_length=30)),
                ('role', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Db_instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=30)),
                ('port', models.CharField(max_length=10)),
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
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='db_account',
            name='dbname',
            field=models.ForeignKey(to='myapp.Db_name'),
        ),
    ]
