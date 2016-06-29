# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0004_auto_20160629_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciclosemestral',
            name='ciclo_semestral',
        ),
        migrations.AddField(
            model_name='ciclosemestral',
            name='nombre',
            field=models.CharField(blank=True, null=True, max_length=100),
            preserve_default=True,
        ),
    ]
