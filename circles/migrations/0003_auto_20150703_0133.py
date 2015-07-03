# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0002_auto_20150617_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='name',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='circle',
            name='owner',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
