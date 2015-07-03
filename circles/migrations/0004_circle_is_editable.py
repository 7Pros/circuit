# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0003_auto_20150703_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='circle',
            name='is_editable',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
