# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0002_auto_20150617_2034'),
        ('posts', '0011_auto_20150619_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='circles',
            field=models.ManyToManyField(to='circles.Circle', related_name='circles', blank=True, null=True),
        ),
    ]
