# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materias',
            name='semestre',
            field=models.ForeignKey(null=True, to='academica.CicloSemestral', blank=True, to_field='clave'),
            preserve_default=True,
        ),
    ]
