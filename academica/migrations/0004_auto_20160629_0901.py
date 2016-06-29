# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0003_auto_20160626_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='CicloSemestral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('clave', models.CharField(max_length=50, blank=True, unique=True)),
                ('ciclo_semestral', models.CharField(max_length=50)),
                ('anio', models.IntegerField(verbose_name='Año')),
                ('periodo', models.IntegerField(blank=True, null=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_termino', models.DateField()),
                ('vigente', models.BooleanField(default=False)),
                ('fecha_inicio_programacion', models.DateField(blank=True, null=True)),
                ('fecha_fin_programacion', models.DateField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='semestre',
            name='anio',
        ),
        migrations.RemoveField(
            model_name='semestre',
            name='ciclo_sep',
        ),
        migrations.RemoveField(
            model_name='semestre',
            name='fecha_inicio',
        ),
        migrations.RemoveField(
            model_name='semestre',
            name='fecha_termino',
        ),
        migrations.RemoveField(
            model_name='semestre',
            name='periodo',
        ),
        migrations.RemoveField(
            model_name='semestre',
            name='vigente',
        ),
        migrations.AddField(
            model_name='semestre',
            name='nombre',
            field=models.CharField(max_length=100, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='semestre',
            name='ciclo_semestral',
            field=models.ForeignKey(to='academica.CicloSemestral', to_field='clave'),
            preserve_default=True,
        ),
    ]
