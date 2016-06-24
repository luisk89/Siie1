# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0002_auto_20160623_2336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semestre',
            options={'ordering': ['clave']},
        ),
        migrations.AddField(
            model_name='semestre',
            name='anio',
            field=models.IntegerField(null=True, blank=True, verbose_name='Año'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semestre',
            name='ciclo_sep',
            field=models.CharField(verbose_name='Ciclo SEP', blank=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semestre',
            name='fecha_fin_programacion',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semestre',
            name='fecha_inicio',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semestre',
            name='fecha_inicio_programacion',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semestre',
            name='fecha_termino',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semestre',
            name='periodo',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semestre',
            name='vigente',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alumnocalificacion',
            name='semestre',
            field=models.ForeignKey(to='academica.Semestre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alumnos',
            name='semestre',
            field=models.ForeignKey(null=True, blank=True, to_field='clave', to='academica.Semestre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bajas',
            name='ciclo',
            field=models.ForeignKey(null=True, blank=True, to_field='clave', to='academica.Semestre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='calificaciones',
            name='semestre',
            field=models.ForeignKey(null=True, to_field='clave', to='academica.Semestre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='creditoeducativo',
            name='semestre',
            field=models.ForeignKey(to='academica.Semestre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupos',
            name='semestre',
            field=models.ForeignKey(null=True, blank=True, to_field='clave', to='academica.Semestre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inscripciones',
            name='semestre',
            field=models.ForeignKey(to='academica.Semestre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='materias',
            name='semestre',
            field=models.ForeignKey(null=True, blank=True, to_field='clave', to='academica.Semestre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='semestre',
            name='ciclo_semestral',
            field=models.CharField(unique=True, blank=True, max_length=50),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='CicloSemestral',
        ),
    ]
