# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0004_auto_20160630_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materias',
            name='semestre',
            field=models.ForeignKey(blank=True, to='academica.Semestre', null=True, to_field='clave'),
            preserve_default=True,
        ),
    ]
