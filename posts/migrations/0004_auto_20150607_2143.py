# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_hashtag_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='post',
        ),
        migrations.AddField(
            model_name='hashtag',
            name='post',
            field=models.ManyToManyField(to='posts.Post'),
        ),
    ]
