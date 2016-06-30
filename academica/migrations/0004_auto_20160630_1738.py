# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0003_auto_20160630_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materias',
            name='semestre',
            field=models.ForeignKey(to_field='clave', blank=True, to='academica.CicloSemestral', null=True),
            preserve_default=True,
        ),
    ]
