# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('username', models.CharField(unique=True, max_length=32)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default='')),
                ('is_active', models.BooleanField(default=False)),
                ('confirm_token', models.CharField(max_length=40, default=users.models.create_hash)),
                ('password_token', models.CharField(max_length=40, default=users.models.create_hash)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
