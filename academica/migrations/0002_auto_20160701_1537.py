# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academica', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnos',
            name='acta_nacimiento',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumnos',
            name='certificado_bachillerato',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumnos',
            name='fotografia_titulo',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumnos',
            name='otro_documento',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='acta_nacimiento',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='actividades_extracurriculares',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='certificado_bachillerato',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='certificado_final',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='constancia_final',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='constancia_servicio',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='curp',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='fotografia_certificado',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='fotografia_infantil',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='fotografia_titulo',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entregadocumentos',
            name='registro_cedula',
            field=models.CharField(blank=True, max_length=25, null=True),
            preserve_default=True,
        ),
    ]
