# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20150619_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reply_original',
            field=models.ForeignKey(null=True, related_name='reply', blank=True, to='posts.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='repost_original',
            field=models.ForeignKey(null=True, related_name='repost', blank=True, to='posts.Post'),
        ),
    ]
