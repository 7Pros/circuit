# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_hashtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashtag',
            name='post',
            field=models.ForeignKey(default=1, to='posts.Post'),
            preserve_default=False,
        ),
    ]
