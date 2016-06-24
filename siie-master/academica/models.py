# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse

from django.db import models


class Aceptados(models.Model):
    alumno_previo = models.ForeignKey('AlumnoPrevio', blank=True, null=True)
    aceptado = models.SmallIntegerField(blank=True, null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class AlumnoCalificacion(models.Model):
    # alumno = models.ForeignKey('Alumnos')
    horario = models.ForeignKey('Horario', blank=True, null=True)
    calificacion = models.IntegerField(blank=True, null=True)
    calificacion_letra = models.CharField(max_length=100, blank=True)
    semestre = models.ForeignKey('CicloSemestral')
    # materia = models.ForeignKey('Materias')
    revalidacion = models.SmallIntegerField(blank=True, null=True)
    ciclo = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["calificacion"]

    def get_absolute_url(self):
        return reverse('list-evaluacion')

    def __str__(self):
        return self.calificacion_letra


class Carreras(models.Model):
    nom_carrera = models.CharField(max_length=50, blank=True)
    clave = models.CharField(max_length=50, blank=True,unique=True)
    abreviatura = models.CharField(max_length=50, blank=True)
    plan_estudio = models.ForeignKey('PlanEstudio', blank=True, null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nom_carrera"]

    def get_absolute_url(self):
        return reverse('list-carrera')

    def __str__(self):
        return self.nom_carrera


class Materias(models.Model):
    nom_materia = models.CharField(max_length=50, blank=True)
    clave = models.CharField(max_length=50, blank=True, unique=True)
    seriacion = models.CharField(max_length=50, blank=True, verbose_name='Serialización')
    creditos = models.IntegerField(blank=True, null=True)
    # carrera = models.ForeignKey("Carreras")
    semestre=models.ForeignKey('Semestre',to_field='clave',null=True,blank=True)
    profesor=models.ForeignKey('Maestros',to_field='no_expediente',null=True,blank=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nom_materia"]

    def get_absolute_url(self):
        return reverse('list-materias')

    def __str__(self):
        return self.nom_materia


class AlumnoPrevio(models.Model):
    alumno = models.ForeignKey("Alumnos", unique=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.alumno.nom_alumno + " " + self.alumno.apellido_paterno + " " + self.alumno.apellido_materno


class AlumnoProyecto(models.Model):
    alumno = models.ForeignKey('Alumnos', blank=True, null=True)
    proyecto = models.ForeignKey('ServicioEstadia', blank=True, null=True)
    concluyo = models.SmallIntegerField(blank=True, null=True)
    calificado = models.SmallIntegerField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Alumnos(models.Model):
    nom_alumno = models.CharField(max_length=200, verbose_name='Nombre', db_index=True)
    apellido_materno = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    curp = models.CharField(max_length=25, blank=True)
    edad = models.IntegerField(blank=True, null=True, )
    sexo = models.CharField(max_length=10, blank=True, verbose_name='genero')
    edo_civil = models.CharField(max_length=50, blank=True, verbose_name='Estado Civil')
    tipo_sangre = models.CharField(max_length=10, blank=True)
    servicio_medico = models.SmallIntegerField(blank=True, null=True)
    instituto = models.CharField(max_length=50, blank=True)
    num_afiliacion = models.CharField(max_length=50, blank=True, verbose_name='No De Afiliación')
    generacion = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True)
    plan = models.ForeignKey('PlanEstudio',to_field='clave_plan',blank=True,null=True)
    no_expediente = models.CharField(max_length=50,blank=True)
    matricula = models.CharField(max_length=20, blank=False, null=False,unique=True)
    semestre = models.ForeignKey('CicloSemestral',to_field='clave', blank=True,null=True)
    condicionado = models.SmallIntegerField(blank=True, null=True,verbose_name='Status')
    domicilio = models.CharField(max_length=100, blank=True)
    colonia = models.CharField(max_length=50, blank=True)
    localidad = models.CharField(max_length=50, blank=True)
    municipio = models.CharField(max_length=50,blank=True,null=True)
    cp = models.CharField(max_length=50, blank=True, verbose_name='Codigo Postal')
    telefono = models.CharField(max_length=50, blank=True)
    lugar_nac = models.CharField(max_length=50, blank=True, null=True, verbose_name='Lugar de nacimiento')
    fecha_nacimiento = models.DateTimeField(blank=True, null=True)
    alergias = models.CharField(max_length=50, blank=True)
    enfermedades = models.CharField(max_length=50, blank=True, verbose_name='Padecimientos')
    contacto_emergencia = models.CharField(max_length=50, blank=True)
    contacto_domicilio = models.CharField(max_length=100, blank=True)
    contacto_tel = models.CharField(max_length=50, blank=True)
    nombre_tutor = models.CharField(max_length=50, blank=True)
    nombre_materno = models.CharField(max_length=50, blank=True)
    domicilio_tutor = models.CharField(max_length=100, blank=True)
    localidad_tutor = models.CharField(max_length=50, blank=True)
    telefono_tutor = models.CharField(max_length=50, blank=True)
    ocupacion_tutor = models.CharField(max_length=50, blank=True)
    sueldo_mensual = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    domicilio_madre = models.CharField(max_length=100, blank=True)
    localidad_madre = models.CharField(max_length=50, blank=True)
    telefono_madre = models.CharField(max_length=50, blank=True)
    trabaja_actualmente = models.BooleanField(default=False)
    puesto = models.CharField(max_length=50, blank=True)
    sueldo_mensual_alumno = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    transporte = models.SmallIntegerField(blank=True, null=True)
    transporte_universidad = models.SmallIntegerField(blank=True, null=True)
    deporte_practica = models.CharField(max_length=50, blank=True)
    musica = models.BooleanField(default=False)
    teatro = models.BooleanField(default=False)
    declamacion = models.BooleanField(default=False)
    oratoria = models.BooleanField(default=False)
    otro_interes = models.BooleanField(default=False,verbose_name='otros')
    credencial = models.SmallIntegerField(blank=True, null=True)
    foto = models.ImageField(upload_to='fotos',blank=True , default='foto.png')
    firma = models.ImageField(upload_to='firma',blank=True)

    escuela_procedencia = models.ForeignKey('Escuela',blank=True, null=True, verbose_name='Escuela')
    anio_egreso=models.CharField(max_length=5,blank=True, null=True,verbose_name='Egreso')
    promedio_bachiller=models.IntegerField(verbose_name='Promedio', null=True, blank=True)

    password = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    extracurriculares = models.ManyToManyField('Extracurriculares', blank=True, null=True)
    is_deuda = models.BooleanField(default=False)

    carrera = models.ForeignKey("Carreras",to_field='clave',blank=True, null=True)
    # nuevos campos
    grupo = models.ForeignKey('Grupos',to_field='clave',blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nom_alumno"]
        permissions = (
            ("can_view_servicios_escolares", "Servicios Escolares"),
        )

    def get_absolute_url(self):
        return reverse('list-alumno')

    def __str__(self):
        return self.nom_alumno + " " + self.apellido_paterno + " " + self.apellido_materno


class Extracurriculares(models.Model):
    nom_materia = models.CharField(max_length=50, blank=True,null=True)
    clave = models.CharField(max_length=50, blank=True,null=True, unique=True)
    tipo = models.CharField(max_length=50, blank=True,null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nom_materia

    def get_absolute_url(self):
        return reverse('list-extra')


class AlumnosAsesorados(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Aulas(models.Model):
    nom_aula = models.CharField(max_length=50, blank=True)
    edificio = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.nom_aula


class Bajas(models.Model):
    matricula = models.ForeignKey(Alumnos,to_field='matricula',null=True,blank=True)
    motivo = models.CharField(max_length=200, blank=True)
    ciclo=models.ForeignKey('CicloSemestral',to_field='clave',null=True,blank=True)
    observaciones=models.CharField(max_length=200,blank=True,null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('baja-add')


class Becas(models.Model):
    nom_beca = models.CharField(max_length=50, blank=True)
    alumnos = models.ManyToManyField('Alumnos', blank=True, null=True)
    tipo_beca = models.ForeignKey('TipoBeca',to_field='clave_tipo_beca')
    limite_becas_total = models.IntegerField(blank=True, null=True, verbose_name="Limite de becas al 100%(Total)")
    restriccion_becas = models.BooleanField(default=False, verbose_name="Restringir capturas de becas(Nuevo Ingreso)")
    restriccion_promedios = models.BooleanField(default=False, verbose_name="Estatus de candados por promedio")
    promedio_80_84 = models.CharField(max_length=50, blank=True,null=True)
    promedio_85_89 = models.CharField(max_length=50, blank=True,null=True)
    promedio_90_94 = models.CharField(max_length=50, blank=True,null=True)
    promedio_95_100 = models.CharField(max_length=50, blank=True,null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nom_beca

    def get_absolute_url(self):
        return reverse('list-beca')


class TipoBeca(models.Model):
    clave_tipo_beca = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=250)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.clave_tipo_beca


class CreditoEducativo(models.Model):
    alumno = models.ForeignKey(Alumnos)
    semestre = models.ForeignKey('CicloSemestral')
    estado = models.SmallIntegerField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Cursos(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    hora = models.DateTimeField(blank=True, null=True)
    instructor = models.CharField(max_length=50, blank=True,null=True)
    personas = models.ManyToManyField("Personas", blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Divisiones(models.Model):
    division = models.CharField(max_length=50, blank=True)
    carreras = models.ManyToManyField('Carreras', blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Documentos(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    alumnos = models.ManyToManyField('Alumnos', blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Empresas(models.Model):
    nombre = models.CharField(max_length=200, blank=True,null=True)
    tipo = models.CharField(max_length=50, blank=True,null=True)
    tamano = models.CharField(max_length=50, blank=True,null=True)
    municipio = models.CharField(max_length=50, blank=True,null=True)
    clave=models.CharField(max_length=50,unique=True,blank=True,null=True)
    direccion=models.CharField(max_length=200, blank=True,null=True)
    telefono=models.CharField(max_length=250, blank=True,null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class EncuestaEgresados(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=50, blank=True)
    carrera = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    edad = models.CharField(max_length=50, blank=True)
    correo_electronico = models.CharField(max_length=50, blank=True)
    estado_civil = models.CharField(max_length=50, blank=True)
    preg_9 = models.CharField(max_length=50, blank=True)
    porque_preg_9 = models.CharField(max_length=50, blank=True)
    preg_10 = models.CharField(max_length=50, blank=True)
    preg_11 = models.CharField(max_length=50, blank=True)
    preg_12 = models.CharField(max_length=50, blank=True)
    preg_13 = models.CharField(max_length=50, blank=True)
    porque_preg_13 = models.CharField(max_length=200, blank=True)
    preg_14 = models.CharField(max_length=50, blank=True)
    porque_preg_14 = models.CharField(max_length=200, blank=True)
    preg_15 = models.CharField(max_length=50, blank=True)
    preg_16 = models.CharField(max_length=100, blank=True)
    preg_17 = models.CharField(max_length=50, blank=True)
    preg_18 = models.CharField(max_length=200, blank=True)
    preg_19 = models.CharField(max_length=50, blank=True)
    preg_20 = models.CharField(max_length=100, blank=True)
    preg_21_1 = models.CharField(max_length=50, blank=True)
    preg_21_2 = models.CharField(max_length=50, blank=True)
    preg_21_3 = models.CharField(max_length=50, blank=True)
    preg_21_4 = models.CharField(max_length=50, blank=True)
    preg_21_5 = models.CharField(max_length=50, blank=True)
    preg_21_6 = models.CharField(max_length=50, blank=True)
    preg_21_7 = models.CharField(max_length=50, blank=True)
    preg_21_8 = models.CharField(max_length=50, blank=True)
    preg_21_9 = models.CharField(max_length=50, blank=True)
    preg_21_10 = models.CharField(max_length=50, blank=True)
    preg_22 = models.CharField(max_length=50, blank=True)
    preg_23 = models.CharField(max_length=50, blank=True)
    preg_24 = models.CharField(max_length=50, blank=True)
    preg_25 = models.CharField(max_length=50, blank=True)
    preg_26 = models.CharField(max_length=50, blank=True)
    preg_27 = models.CharField(max_length=50, blank=True)
    preg_28 = models.CharField(max_length=50, blank=True)
    porque_preg_28 = models.CharField(max_length=200, blank=True)
    preg_29 = models.CharField(max_length=50, blank=True)
    preg_30 = models.CharField(max_length=50, blank=True)
    porque_preg_30 = models.CharField(max_length=200, blank=True)
    preg_31_1 = models.CharField(max_length=50, blank=True)
    preg_31_2 = models.CharField(max_length=50, blank=True)
    preg_31_3 = models.CharField(max_length=50, blank=True)
    preg_31_4 = models.CharField(max_length=50, blank=True)
    preg_31_5 = models.CharField(max_length=50, blank=True)
    preg_31_6 = models.CharField(max_length=50, blank=True)
    preg_31_7 = models.CharField(max_length=50, blank=True)
    preg_31_8 = models.CharField(max_length=50, blank=True)
    preg_31_9 = models.CharField(max_length=50, blank=True)
    preg_31_10 = models.CharField(max_length=50, blank=True)
    preg_31_11 = models.CharField(max_length=50, blank=True)
    porque_preg_31_1 = models.CharField(max_length=50, blank=True)
    porque_preg_31_2 = models.CharField(max_length=50, blank=True)
    preg_32 = models.CharField(max_length=50, blank=True)
    preg_33_1 = models.CharField(max_length=50, blank=True)
    preg_33_2 = models.CharField(max_length=50, blank=True)
    preg_33_3 = models.CharField(max_length=50, blank=True)
    preg_33_4 = models.CharField(max_length=50, blank=True)
    preg_34_1 = models.CharField(max_length=50, blank=True)
    preg_34_2 = models.CharField(max_length=50, blank=True)
    preg_34_3 = models.CharField(max_length=50, blank=True)
    preg_34_4 = models.CharField(max_length=50, blank=True)
    preg_34_5 = models.CharField(max_length=50, blank=True)
    preg_34_6 = models.CharField(max_length=50, blank=True)
    preg_34_7 = models.CharField(max_length=50, blank=True)
    preg_34_8 = models.CharField(max_length=50, blank=True)
    preg_34_9 = models.CharField(max_length=50, blank=True)
    preg_34_10 = models.CharField(max_length=50, blank=True)
    preg_34_11 = models.CharField(max_length=50, blank=True)
    preg_34_12 = models.CharField(max_length=50, blank=True)
    preg_35_1 = models.CharField(max_length=50, blank=True)
    preg_35_2 = models.CharField(max_length=50, blank=True)
    preg_35_3 = models.CharField(max_length=50, blank=True)
    preg_35_4 = models.CharField(max_length=50, blank=True)
    preg_36 = models.CharField(max_length=200, blank=True)
    preg_37 = models.CharField(max_length=200, blank=True)
    preg_38_1 = models.CharField(max_length=50, blank=True)
    preg_38_2 = models.CharField(max_length=50, blank=True)
    preg_38_3 = models.CharField(max_length=50, blank=True)
    preg_38_4 = models.CharField(max_length=50, blank=True)
    preg_38_5 = models.CharField(max_length=50, blank=True)
    preg_39 = models.CharField(max_length=100, blank=True)
    preg_40 = models.CharField(max_length=50, blank=True)
    preg_41 = models.CharField(max_length=50, blank=True)
    porque_preg_41 = models.CharField(max_length=200, blank=True)
    preg_42 = models.CharField(max_length=50, blank=True)
    porque_preg_42 = models.CharField(max_length=200, blank=True)
    comentarios = models.CharField(max_length=200, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class EncuestaEmpleador(models.Model):
    empresa = models.CharField(max_length=50, blank=True)
    responsable = models.CharField(max_length=50, blank=True)
    puesto = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    correo = models.CharField(max_length=50, blank=True)
    preg_2 = models.CharField(max_length=50, blank=True)
    preg_3 = models.CharField(max_length=50, blank=True)
    preg_4 = models.CharField(max_length=50, blank=True)
    porque_preg_4 = models.CharField(max_length=50, blank=True)
    preg_5 = models.CharField(max_length=200, blank=True)
    preg_6 = models.CharField(max_length=200, blank=True)
    preg_7 = models.CharField(max_length=200, blank=True)
    preg_8_1 = models.CharField(max_length=50, blank=True)
    preg_8_2 = models.CharField(max_length=50, blank=True)
    preg_8_3 = models.CharField(max_length=50, blank=True)
    preg_8_4 = models.CharField(max_length=50, blank=True)
    preg_8_5 = models.CharField(max_length=50, blank=True)
    preg_8_6 = models.CharField(max_length=50, blank=True)
    preg_8_7 = models.CharField(max_length=50, blank=True)
    preg_8_8 = models.CharField(max_length=50, blank=True)
    preg_8_9 = models.CharField(max_length=50, blank=True)
    preg_8_10 = models.CharField(max_length=50, blank=True)
    preg_8_11 = models.CharField(max_length=50, blank=True)
    preg_8_12 = models.CharField(max_length=50, blank=True)
    preg_8_13 = models.CharField(max_length=50, blank=True)
    preg_8_14 = models.CharField(max_length=50, blank=True)
    preg_8_15 = models.CharField(max_length=50, blank=True)
    preg_8_16 = models.CharField(max_length=50, blank=True)
    preg_8_17 = models.CharField(max_length=50, blank=True)
    preg_8_18 = models.CharField(max_length=50, blank=True)
    preg_8_19 = models.CharField(max_length=50, blank=True)
    preg_8_20 = models.CharField(max_length=50, blank=True)
    preg_8_21 = models.CharField(max_length=50, blank=True)
    preg_8_22 = models.CharField(max_length=50, blank=True)
    preg_9 = models.CharField(max_length=200, blank=True)
    preg_10_1 = models.CharField(max_length=50, blank=True)
    preg_10_2 = models.CharField(max_length=50, blank=True)
    preg_10_3 = models.CharField(max_length=50, blank=True)
    preg_11 = models.CharField(max_length=200, blank=True)
    preg_12 = models.CharField(max_length=200, blank=True)
    preg_13 = models.CharField(max_length=50, blank=True)
    porque_preg_13 = models.CharField(max_length=200, blank=True)
    preg_14 = models.CharField(max_length=200, blank=True)
    comentarios = models.CharField(max_length=200, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class EntregaDocumentos(models.Model):
    alumno = models.ForeignKey(Alumnos)
    acta_nacimiento = models.SmallIntegerField(blank=True, null=True)
    certificado_bachillerato = models.SmallIntegerField(blank=True, null=True)
    certificado_final = models.SmallIntegerField(blank=True, null=True)
    constancia_final = models.SmallIntegerField(blank=True, null=True)
    constancia_servicio = models.SmallIntegerField(blank=True, null=True)
    curp = models.SmallIntegerField(blank=True, null=True)
    actividades_extracurriculares = models.SmallIntegerField(blank=True, null=True)
    fotografia_titulo = models.SmallIntegerField(blank=True, null=True)
    fotografia_certificado = models.SmallIntegerField(blank=True, null=True)
    fotografia_infantil = models.SmallIntegerField(blank=True, null=True)
    registro_cedula = models.SmallIntegerField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Equipos(models.Model):
    num_serie = models.CharField(max_length=50, blank=True)
    nombre = models.CharField(max_length=50, blank=True)
    laboratorio = models.ForeignKey('LaboratorioComputo', blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Estados(models.Model):
    nom_estado = models.CharField(max_length=50, blank=True)
    clave = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="activo")

    class Meta:
        ordering = ["nom_estado"]

    def __str__(self):
        return self.nom_estado


class Estatus(models.Model):
    nombre = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class ExtraHorario(models.Model):
    extracurricular = models.ForeignKey('Extracurriculares')
    lunes_hora = models.DateTimeField(blank=True, null=True)
    martes_hora = models.DateTimeField(blank=True, null=True)
    miercoles_hora = models.DateTimeField(blank=True, null=True)
    jueves_hora = models.DateTimeField(blank=True, null=True)
    viernes_hora = models.DateTimeField(blank=True, null=True)
    lunes_duracion = models.DateTimeField(blank=True, null=True)
    martes_duracion = models.DateTimeField(blank=True, null=True)
    miercoles_duracion = models.DateTimeField(blank=True, null=True)
    jueves_duracion = models.DateTimeField(blank=True, null=True)
    viernes_duracion = models.DateTimeField(blank=True, null=True)
    id_maestro = models.BigIntegerField(blank=True, null=True)
    nom_horario = models.CharField(max_length=50, blank=True)
    periodo = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Grupos(models.Model):
    clave = models.CharField(max_length=50,blank=True,unique=True)
    nombre = models.CharField(max_length=50, blank=True)
    cant_alumnos = models.IntegerField(blank=True, null=True)
    semestre = models.ForeignKey("CicloSemestral",to_field='clave',blank=True,null=True)
    #carrera = models.ForeignKey('Carreras',to_field='clave',blank=True,null=True)
    actual = models.SmallIntegerField(blank=True, null=True)
    ciclo_escolar = models.CharField(max_length=50, blank=True)
    plan = models.ForeignKey('PlanEstudio',to_field='clave_plan',blank=True, null=True)
    #el plan tiene las materias
    #materias = models.ManyToManyField("Materias", blank=True, null=True)
    # maestros = models.ManyToManyField("Maestros", blank=True, null=True)

    # nuevos campos
    #horario = models.ForeignKey("Horario", blank=True, null=True)
    horarios = models.ManyToManyField("Horario", blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def get_absolute_url(self):
        return reverse('list-grupos')

    def __str__(self):
        return self.clave


class Horario(models.Model):
    clave_horario = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    hora_inicio = models.CharField(max_length=2, blank=True, null=True)
    hora_termino = models.CharField(max_length=2, blank=True, null=True)
    minutos_inicio = models.CharField(max_length=2, blank=True, null=True)
    minutos_termino = models.CharField(max_length=2, blank=True, null=True)
    aula = models.ForeignKey('Aulas', blank=True, null=True)
    profesores = models.ForeignKey('Maestros', blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="activo")

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["aula"]

    def get_absolute_url(self):
        return reverse('list-horario')


class Inscripciones(models.Model):
    alumno = models.ForeignKey('Alumnos')
    semestre = models.ForeignKey('CicloSemestral')

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Jefes(models.Model):
    nom_jefe = models.CharField(max_length=50, blank=True)
    puesto = models.CharField(max_length=50, blank=True)
    firma = models.BinaryField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class JefesDivision(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    division = models.ForeignKey('Divisiones')
    usuario = models.ForeignKey('Usuarios', blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class LaboratorioComputo(models.Model):
    nom_laboratorio = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class LiberacionDocumentos(models.Model):
    acta_nacimiento = models.SmallIntegerField(blank=True, null=True)
    certificado_bachillerato = models.SmallIntegerField(blank=True, null=True)
    certificado_final = models.SmallIntegerField(blank=True, null=True)
    constancia_final = models.SmallIntegerField(blank=True, null=True)
    constancia_servicio = models.SmallIntegerField(blank=True, null=True)
    curp = models.SmallIntegerField(blank=True, null=True)
    alumno = models.ForeignKey('Alumnos')

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Maestros(models.Model):
    nombre = models.CharField(max_length=50, blank=True, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Apellido')
    no_expediente = models.CharField(max_length=50, blank=False, verbose_name='Numero de Empleado', unique=True)
    email = models.EmailField(default='email@email.com',unique=True)
    foto = models.ImageField(upload_to='fotos', blank=True , verbose_name='Foto', default='foto.png')
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def get_absolute_url(self):
        return reverse('list-maestro')

    def __str__(self):
        return self.nombre


class Municipios(models.Model):
    nom_municipio = models.CharField(max_length=50, blank=True)
    estado = models.ForeignKey('Estados',blank=True,null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nom_municipio


class Personas(models.Model):
    nom_persona = models.CharField(max_length=50, blank=True)
    edad = models.IntegerField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class PlanEstudio(models.Model):
    nom_plan = models.CharField(max_length=50, blank=True)
    clave_plan = models.CharField(max_length=50, blank=True, unique=True)
    materias = models.ManyToManyField("Materias", blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.clave_plan

    class Meta:
        ordering = ["nom_plan"]

    def get_absolute_url(self):
        return reverse('list-planEstudio')


class Privilegios(models.Model):
    privilegio = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class ProgramacionExamen(models.Model):
    alumno = models.ForeignKey('Alumnos')

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class ReservacionAlumno(models.Model):
    alumno = models.BigIntegerField(blank=True, null=True)
    equipo = models.BigIntegerField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class ReservacionMaestroEsporadico(models.Model):
    maestro = models.ForeignKey('Maestros', blank=True, null=True)
    laboratorio = models.ForeignKey('LaboratorioComputo', blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class ReservacionMaestroFijo(models.Model):
    maestro = models.ForeignKey('Maestros', blank=True, null=True)
    laboratorio = models.ForeignKey('LaboratorioComputo', blank=True, null=True)
    hora_lunes_inicio = models.DateTimeField(blank=True, null=True)
    hora_martes_inicio = models.DateTimeField(blank=True, null=True)
    hora_miercoles_inicio = models.DateTimeField(blank=True, null=True)
    hora_jueves_inicio = models.DateTimeField(blank=True, null=True)
    hora_viernes_inicio = models.DateTimeField(blank=True, null=True)
    hora_lunes_fin = models.DateTimeField(blank=True, null=True)
    hora_martes_fin = models.DateTimeField(blank=True, null=True)
    hora_miercoles_fin = models.DateTimeField(blank=True, null=True)
    hora_jueves_fin = models.DateTimeField(blank=True, null=True)
    hora_viernes_fin = models.DateTimeField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Revalidaciones(models.Model):
    alumno = models.ForeignKey('Alumnos')
    tipo = models.CharField(max_length=50, blank=True)
    materia = models.ForeignKey('Materias')

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class ServicioEstadia(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    asesor_interno = models.CharField(max_length=50, blank=True)
    asesor_externo = models.CharField(max_length=50, blank=True)
    empresa = models.ForeignKey('Empresas')
    tipo = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class ServicioHoras(models.Model):
    alumno = models.ForeignKey('Alumnos',unique=True)
    proyecto = models.ForeignKey('ServicioEstadia')
    horas = models.IntegerField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='liberar')

    def __str__(self):
        return self.proyecto.nombre

    def get_absolute_url(self):
        return reverse('list-servicio')


class Servicios(models.Model):
    nombre = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class SolicitudBeca(models.Model):
    beca = models.ForeignKey('Becas')
    alumno = models.ForeignKey('Alumnos')
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=1)
    principal = models.IntegerField()
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class TemasTitulo(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    alumno = models.ForeignKey('Alumnos')
    aceptado = models.SmallIntegerField(blank=True, null=True)
    asesor = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Titulos(models.Model):
    tema = models.ForeignKey('TemasTitulo')
    hora_inicio = models.DateTimeField(blank=True, null=True)
    hora_fin = models.DateTimeField(blank=True, null=True)
    dictamen = models.CharField(max_length=50, blank=True)
    no_foja = models.IntegerField(blank=True, null=True)
    tipo_folio = models.CharField(max_length=50, blank=True)
    no_libro = models.CharField(max_length=50, blank=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class TmpAlumnoServicio(models.Model):
    alumno = models.ForeignKey('Alumnos', blank=True, null=True)
    horas = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('Usuarios', blank=True, null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class TmpAlumnosEstadias(models.Model):
    alumno = models.ForeignKey('Alumnos', blank=True, null=True)
    user = models.ForeignKey('Usuarios', blank=True, null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Tramites(models.Model):
    alumno = models.ForeignKey('Alumnos')
    estatus = models.ForeignKey('Estatus')
    servicio = models.ForeignKey('Servicios')
    monto = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Usuarios(models.Model):
    usuario = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=100, blank=True)
    privilegio = models.ForeignKey('Privilegios')
    maestro = models.ForeignKey('Maestros')
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class UsuariosLab(models.Model):
    usuario = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=True)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Evaluacion(models.Model):
    materia = models.ForeignKey('Materias')
    alumno = models.ForeignKey('Alumnos')
    calificacion = models.ForeignKey('AlumnoCalificacion')

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('list-evaluacion')

class Semestre(models.Model):
    ciclo_semestral=models.ForeignKey('CicloSemestral',to_field='clave')
    clave = models.CharField(max_length=50,blank=True,unique=True)


    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('list-sem')

class CicloSemestral(models.Model):
    clave = models.CharField(max_length=50,blank=True,unique=True)
    ciclo_sep = models.CharField(max_length=50, blank=True, verbose_name='Ciclo SEP')
    anio = models.IntegerField(blank=True, null=True, verbose_name="Año")
    periodo = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_termino = models.DateTimeField(blank=True, null=True)
    vigente = models.BooleanField(default=False)

    fecha_inicio_programacion = models.DateTimeField(blank=True, null=True)
    fecha_fin_programacion = models.DateTimeField(blank=True, null=True)

    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["clave"]

    def get_absolute_url(self):
        return reverse('list-semestre')

    def __str__(self):
        return self.clave


class Biblioteca(models.Model):
    alumno = models.ForeignKey('Alumnos', unique=True)
    observacion = models.CharField(max_length=250,blank=True, null=True, verbose_name="Observaciones")

    alta_date_created = models.DateTimeField(verbose_name='Alta de adeudo',blank=True, null=True)
    baja_date_created = models.DateTimeField(blank=True, null=True, verbose_name='Baja de adeudo')
    is_active = models.BooleanField(default=True, verbose_name='Deuda Activa')

    def get_absolute_url(self):
        return reverse('list-biblio')

    def __str__(self):
        return "Deuda Biblioteca #"+self.id.__str__()



class CentroComputo(models.Model):
    alumno = models.ForeignKey('Alumnos', unique=True)
    observacion = models.CharField(max_length=250,blank=True, null=True, verbose_name="Observaciones")

    alta_date_created = models.DateTimeField(verbose_name='Alta de adeudo',blank=True, null=True)
    baja_date_created = models.DateTimeField(blank=True, null=True, verbose_name='Baja de adeudo')
    is_active = models.BooleanField(default=True,verbose_name='Deuda Activa')

    def __str__(self):
        return "Deuda CC #"+self.id.__str__()

    def get_absolute_url(self):
        return reverse('list-cc')

class Contabilidad(models.Model):
    alumno = models.ForeignKey('Alumnos', unique=True)
    observacion = models.CharField(max_length=250,blank=True, null=True, verbose_name="Observaciones")

    alta_date_created = models.DateTimeField(verbose_name='Alta de adeudo')
    baja_date_created = models.DateTimeField(blank=True, null=True, verbose_name='Baja de adeudo')
    is_active = models.BooleanField(default=True,verbose_name='Deuda Activa')

    def __str__(self):
        return "Deuda Contabilidad #"+self.id__str__()

    def get_absolute_url(self):
        return reverse('list-conta')

class Escuela(models.Model):
    estado=models.ForeignKey('Estados')
    localidad=models.CharField(max_length=50, blank=True, null=True)
    nombre=models.CharField(max_length=100)
    alta_date_created = models.DateTimeField(auto_now_add=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


    def get_absolute_url(self):
        return reverse('alumno-add')

    def __str__(self):
        return self.nombre

class Calificaciones(models.Model):

    #carrera?
    materia = models.ForeignKey(Materias,to_field='clave',null=True)
    matricula = models.ForeignKey(Alumnos,to_field='matricula',null=True)
    semestre = models.ForeignKey(CicloSemestral,to_field='clave',null=True)
    plan = models.ForeignKey(PlanEstudio,to_field='clave_plan',null=True)


    primera = models.DecimalField(max_digits=3, decimal_places=0, blank=True, verbose_name='1ra Calificacion', null=True, )
    status1 = models.IntegerField(blank=True, null=True, verbose_name='Status')

    segunda = models.DecimalField(max_digits=3, decimal_places=0, blank=True, verbose_name='2da Calificacion', null=True, )
    status2 = models.IntegerField(blank=True, verbose_name='Status', null=True)

    tercera = models.DecimalField(max_digits=3, decimal_places=0, blank=True, verbose_name='3ra Calificacion',null=True, )
    status3 = models.IntegerField(blank=True, verbose_name='Status', null=True, )

    cuarta = models.DecimalField(max_digits=3, decimal_places=0, blank=True, verbose_name='4ta Calificacion',null=True, )
    status4 = models.IntegerField(blank=True, verbose_name='Status', null=True, )

    quinta = models.DecimalField(max_digits=3, decimal_places=0, blank=True, verbose_name='5ta Calificacion', null=True, )
    status5 = models.IntegerField(blank=True, verbose_name='Status', null=True, )

    sexta = models.DecimalField(max_digits=3, decimal_places=0, blank=True, verbose_name='6ta Calificacion',null=True, )
    status6 = models.IntegerField(blank=True, verbose_name='Status', null=True, )

    final = models.DecimalField(max_digits=3, decimal_places=0, blank=True, verbose_name='Calificacion Final',null=True, )
    status_final = models.IntegerField(blank=True, verbose_name='Status', null=True, )

    borrado = models.IntegerField(blank=True, null=True, )
    tipoacreditacion = models.IntegerField(blank=True, null=True, )
    actualizado = models.DateTimeField(blank=True, null=True, )
    fecha_revalidacion = models.DateTimeField(blank=True, null=True, )
    fecha_modificacion = models.DateTimeField(blank=True, null=True,auto_now_add=True )
    modulo = models.IntegerField(blank=True, null=True, )
    login = models.CharField(max_length=20, blank=True, null=True, )


    claveubicacion = models.CharField(max_length=10, blank=True, null=True, )
    id_curso = models.IntegerField(blank=True, null=True, )
    fecha_extraordinario = models.DateTimeField(blank=True, null=True, )

    alta_date_created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    baja_date_created = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('list-calificacion')

    def __str__(self):
        return self.matricula + self.materia