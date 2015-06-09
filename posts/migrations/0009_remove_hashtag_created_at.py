# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='created_at',
        ),
    ]
