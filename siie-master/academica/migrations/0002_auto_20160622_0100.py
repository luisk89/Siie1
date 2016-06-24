# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='materias',
            name='profesor',
            field=models.ForeignKey(blank=True, null=True, to='academica.Maestros', to_field='no_expediente'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maestros',
            name='no_expediente',
            field=models.CharField(verbose_name='Numero de Empleado', blank=True, max_length=50, unique=True),
            preserve_default=True,
        ),
    ]
