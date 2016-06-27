# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('academica', '0002_auto_20160626_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumnoprevio',
            name='alumno',
            field=models.ForeignKey(to='academica.Alumnos'),
            preserve_default=True,
        ),
    ]
