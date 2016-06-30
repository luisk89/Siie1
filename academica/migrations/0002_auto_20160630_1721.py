# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='planestudio',
            name='duracion',
            field=models.CharField(null=True, blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planestudio',
            name='modalidad',
            field=models.CharField(null=True, blank=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planestudio',
            name='objetivo',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
