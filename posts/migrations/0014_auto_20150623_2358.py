# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0002_auto_20150617_2034'),
        ('posts', '0013_auto_20150623_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='circles',
        ),
        migrations.AddField(
            model_name='post',
            name='circles',
            field=models.ForeignKey(null=True, related_name='circles', blank=True, to='circles.Circle'),
        ),
    ]
