# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('permissions_estudiante', 'Permiso para los Estudiantes'), ('permissions_administrador', 'Permiso para los Administradores'), ('permissions_maestros', 'Permiso para los Maestros'), ('permissions_biblioteca', 'Permiso para Biblioteca'), ('permissions_centro_computo', 'Permiso para Centro Computo'), ('permissions_contabilidad', 'Permiso para Contabilidad'))},
        ),
    ]
