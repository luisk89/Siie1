# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('academica', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumnoprevio',
            name='alumno',
            field=models.ForeignKey(blank=True, to='academica.Alumnos'),
            preserve_default=True,
        ),
    ]
