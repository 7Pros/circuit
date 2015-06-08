# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True,
                                       default=datetime.datetime(2015, 6, 5, 16, 35, 9, 486052, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
