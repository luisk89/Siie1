# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0002_auto_20160701_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregadocumentos',
            name='alumno',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
