# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20150607_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='post',
        ),
        migrations.AddField(
            model_name='hashtag',
            name='postsp1',
            field=models.ManyToManyField(to='posts.Post'),
        ),
    ]
