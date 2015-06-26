# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_remove_hashtag_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='original_post',
            new_name='repost_original',
        ),
    ]
