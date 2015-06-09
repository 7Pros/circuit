# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='original_post',
            field=models.ForeignKey(blank=True, null=True, to='posts.Post'),
        ),
    ]
