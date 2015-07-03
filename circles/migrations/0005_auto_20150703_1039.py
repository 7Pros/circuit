# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0004_circle_is_editable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='is_editable',
            field=models.BooleanField(default=True),
        ),
    ]
