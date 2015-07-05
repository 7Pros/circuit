# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_notification_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.IntegerField(default=1, choices=[(0, 'circle-related'), (1, 'post-related')]),
        ),
    ]
