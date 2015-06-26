# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_post_circles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='circles',
            field=models.ManyToManyField(related_name='circles', to='circles.Circle', blank=True),
        ),
    ]
