# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='circle',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 6, 17, 18, 33, 58, 802301, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='circle',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 6, 17, 18, 34, 9, 551374, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
