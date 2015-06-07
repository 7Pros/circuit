# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20150607_2219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hashtag',
            old_name='postsp1',
            new_name='posts',
        ),
    ]
