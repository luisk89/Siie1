# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materias',
            name='profesor',
        ),
        migrations.AddField(
            model_name='materias',
            name='profesores',
            field=models.ManyToManyField(blank=True, to='academica.Maestros', null=True),
            preserve_default=True,
        ),
    ]
