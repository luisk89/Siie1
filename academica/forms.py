# -*- encoding: utf-8 -*-
import datetime
from django.contrib.admin import widgets
from django.db.models.fields import DateField
from django.forms.fields import CharField
from django.forms.widgets import Textarea, TextInput
from django.utils import timezone
from academica import mixins

__author__ = 'Luisk'
from django import forms
from django.forms.util import ErrorList
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Div, HTML
from crispy_forms.bootstrap import TabHolder, Tab, InlineField, InlineCheckboxes



from academica.models import Alumnos, PlanEstudio, Extracurriculares, Grupos, Horario, Materias, Maestros, \
    Carreras, Bajas, Evaluacion, EncuestaEgresados, Aulas, Municipios, \
    Estados, Calificaciones, ServicioHoras, Becas, TipoBeca, Escuela, Biblioteca, Contabilidad, CentroComputo, Semestre, \
    CicloSemestral, EntregaDocumentos
from users.models import User

class ExtraCurricularesForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        'nom_materia', 'clave', 'tipo'
    )

    class Meta:
        model = Extracurriculares
        fields = '__all__'


GENERO_SELECT = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),

)
Estado_Civil = (
    ('Soltero', 'Soltero'),
    ('Casado', 'Casado'),
)
Servicio_medico = (
    ('1', 'IMSS UNISIERRA'),
    ('2', 'IMSS'),
    ('3', 'ISSSTESON'),
    ('4', 'ISSSTE'),
    ('5', 'SEGURO POPULAR'),
    ('6', 'PARTICULAR')
)

Condicionado_select = (
    ('1', 'Normal'),
    ('2', 'Revalidacion'),
    ('3', 'Equivalencia'),
    ('4', 'Convalidación')
)
Sangre_select = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-')

)


DIAS_SELECT = (
    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miercoles', 'Miercoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sabado', 'Sabado'),
    ('Domingo', 'Domingo'),

)
WHITE_SPACE = (
    ('-', '----------'),
)
TIPO_DOC = (
    ('Original', 'Original'),
    ('Copia', 'Copia'),
    ('Ninguno', 'Ninguno'),
    ('Otro', 'Otro')
)

hoy = datetime.datetime.now()
hoy = hoy.strftime('%Y-%m-%d')
style_numeric = 'ui-widget ui-widget-content numeric-field'

from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class AlumnosForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = '__all__'


        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa','class': 'datepicker ui-widget ui-widget-content date-field'}),
        }
    sexo = forms.ChoiceField(choices=GENERO_SELECT,
                             widget=forms.Select(), required=False, label='Genero')
    edo_civil = forms.ChoiceField(choices=Estado_Civil,
                                  widget=forms.Select(), required=False, label='Estado Civil')
    servicio_medico = forms.ChoiceField(choices=Servicio_medico,
                                        widget=forms.Select(), required=False)
    condicionado = forms.ChoiceField(choices=Condicionado_select,
                                     widget=forms.Select(), required=False, initial='Normal', label='Status')

    tipo_sangre = forms.ChoiceField(choices=Sangre_select,
                                    widget=forms.Select(), required=False)
    edad = forms.IntegerField(required=False)
    promedio_bachiller=forms.FloatField(label='Promedio', widget=forms.TextInput(attrs={'class':style_numeric}), required=False)
    curp=forms.CharField(max_length=18,min_length=18,required=False)

    acta_nacimiento = forms.ChoiceField(choices=TIPO_DOC,
                                        widget=forms.Select(), required=False, initial='Normal',
                                        label='Acta de nacimiento')
    certificado_bachillerato = forms.ChoiceField(choices=TIPO_DOC,
                                                 widget=forms.Select(), required=False, initial='Normal',
                                                 label='Cert.Bachillerato')
    fotografia_titulo = forms.ChoiceField(choices=TIPO_DOC,
                                          widget=forms.Select(), required=False, initial='Normal', label='Fotografia')

    is_active=forms

    def __init__(self, *args, **kwargs):
        super(AlumnosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['edad'].widget.attrs['min'] = 1
        self.fields['sueldo_mensual'].widget.attrs['min'] = 0
        self.fields['sueldo_mensual_alumno'].widget.attrs['min'] = 0
        self.fields['is_active'].widget = forms.HiddenInput()
        self.fields['trabaja_actualmente'].widget.attrs['onchange']="javascript:showContent1()"
        self.fields['carrera'].widget.attrs['onchange']="javascript:Buscar()"
        self.fields['matricula'].widget.attrs['placeholder']="AACCCC"
        self.fields['municipio'].widget.attrs['onchange'] = "javascript:cambiarLocalidad();"
        self.fields['estado'].widget.attrs['onchange'] = "javascript:cambiarMunicipio();"
        self.fields['municipio'].widget.attrs['disabled'] = True
        self.fields['alergias'].initial = 'NINGUNO'
        self.fields['enfermedades'].initial = 'NINGUNO'
        self.fields['domicilio'].label='Calle y N°'
        self.fields['anio_egreso'].label = 'Año de Egreso'

        is_insert = self.instance.pk is None
        if is_insert:
            self.fields['matricula'].widget.attrs['onfocus'] = "javascript:Buscar()"
            self.fields['plan'].widget.attrs['onchange'] = "javascript:Buscar()"
            self.fields['semestre'].widget.attrs['onchange'] = "javascript:Buscar()"

        else:
            self.fields['email'].widget.attrs['readonly'] = "readonly"
            self.fields['matricula'].widget.attrs['readonly'] = "readonly"
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))


        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Datos Personales',
                    'is_active',
                    'nom_alumno',
                    'apellido_paterno',
                    'apellido_materno',
                    Fieldset('Credencial', 'foto', 'firma', id='img'),
                    'curp',
                    'sexo',
                    'edad',
                    'lugar_nac',
                    'fecha_nacimiento',
                    'edo_civil',
                    Fieldset('Datos medicos', 'tipo_sangre', 'alergias', 'enfermedades', HTML("""<div id="div_id_seguro" class="checkbox"> <label for="id_seguro" class=""> <input checked="checked" class="checkboxinput" id="id_seguro" name="seguro" type="checkbox" value="1" onchange="javascript:showContent()">
                    Servicio Medico</label> </div>"""), Div('num_afiliacion', 'servicio_medico', id='div_ServicioMedico')),
                    Fieldset('Domicilio','domicilio', 'colonia', 'estado', 'municipio', HTML(
                        """<div class="form-group" id="div_id_localidad"> <label class="control-label form-group" for="id_localidad">Localidad</label> <div class="controls "> <select " name="localidad" id="id_localidad" class="select form-control" disabled="True" ><option selected="selected" value="">---------</option></select> </div> </div>"""),
                             'telefono', 'cp',
                             id='domicilio'),
                     Fieldset('Correo','email')
                ),

                Tab(
                    'Datos Escolares',
                    Fieldset('Procedencia',HTML("""<a data-toggle="modal"
                        data-target="#modalEscuela"
                        id="modal-button"><i class="fa fa-plus-circle"></i></a>"""), 'escuela_procedencia',
                             'anio_egreso', 'promedio_bachiller'),
                    Fieldset('Control Escolar', 'plan', 'semestre', 'matricula', 'condicionado', 'grupo'),

                    css_class="nav nav-tabs"
                ),
                Tab(
                    'Documentacion y Datos Varios',
                    Fieldset('En caso de emergencia avisar a:', 'contacto_emergencia', 'contacto_domicilio',
                             'contacto_tel'),
                    Fieldset('Datos Familiares',
                             Fieldset('Datos del padre o tutor', 'nombre_tutor', 'domicilio_tutor', 'localidad_tutor',
                                      'telefono_tutor', 'ocupacion_tutor', 'sueldo_mensual', HTML(
                                     """<a class="btn btn-success" id='id_boton_copiar' onclick="javascript:datacopy()"><i class="fa fa-copy"></i>Copiar datos a la madre</a>""")),
                             Fieldset('Datos de la madre', 'nombre_materno', 'domicilio_madre', 'localidad_madre',
                                      'telefono_madre'),
                             Fieldset('Datos generales', 'trabaja_actualmente',
                                      Div('puesto', 'sueldo_mensual_alumno', id='div_trabajo_estudiante'))),
                    Fieldset('Entrega de documentos', 'acta_nacimiento', 'certificado_bachillerato',
                             'fotografia_titulo', 'otro_documento'),
                    Fieldset('Actividades', 'deporte_practica'),
                    Div('oratoria', 'musica',
                        'teatro', 'declamacion', 'otro_interes'),
                    Fieldset('Transporte', 'transporte', 'transporte_universidad'),

                    css_class="nav nav-tabs"
                ),

                css_class="nav-tabs-custom"
            )

        )

    def clean_email(self):
        email = self.cleaned_data['email']
        is_insert = self.instance.pk is None
        if is_insert:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError("Existe un usuario con este email por favor cambiarlo")
        else:
            self.fields['email'].widget.attrs['readonly'] = "readonly"
        return email

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        is_insert = self.instance.pk is None
        if is_insert:
            try:
                User.objects.get(no_expediente=matricula)
            except User.DoesNotExist:
                return matricula
            raise forms.ValidationError("Existe un usuario con esta matricula por favor cambiarlo")
        else:
            self.fields['matricula'].widget.attrs['readonly'] = "readonly"
        return matricula

class ReinscripcionAlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = '__all__'


        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa','class': 'datepicker ui-widget ui-widget-content date-field'}),
        }



    sexo = forms.ChoiceField(choices=GENERO_SELECT,
                             widget=forms.Select(), required=False, label='Genero')
    edo_civil = forms.ChoiceField(choices=Estado_Civil,
                                  widget=forms.Select(), required=False, label='Estado Civil')
    servicio_medico = forms.ChoiceField(choices=Servicio_medico,
                                        widget=forms.Select(), required=False)
    condicionado = forms.ChoiceField(choices=Condicionado_select,
                                     widget=forms.Select(), required=False, initial='Normal', label='Status')

    tipo_sangre = forms.ChoiceField(choices=Sangre_select,
                                    widget=forms.Select(), required=False)
    edad = forms.IntegerField(required=False)
    promedio_bachiller = forms.FloatField(label='Promedio', widget=forms.TextInput(attrs={'class': style_numeric}),required=False)
    curp=forms.CharField(max_length=18,required=False)

    acta_nacimiento = forms.ChoiceField(choices=TIPO_DOC,
                                        widget=forms.Select(), required=False, initial='Normal',
                                        label='Acta de nacimiento')
    certificado_bachillerato = forms.ChoiceField(choices=TIPO_DOC,
                                                 widget=forms.Select(), required=False, initial='Normal',
                                                 label='Cert.Bachillerato')
    fotografia_titulo = forms.ChoiceField(choices=TIPO_DOC,
                                          widget=forms.Select(), required=False, initial='Normal', label='Fotografia')

    def __init__(self, *args, **kwargs):
        super(ReinscripcionAlumnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['edad'].widget.attrs['min'] = 1
        self.fields['sueldo_mensual'].widget.attrs['min'] = 0
        self.fields['sueldo_mensual_alumno'].widget.attrs['min'] = 0
        self.fields['is_active'].widget = forms.HiddenInput()
        self.fields['is_active'].initial = True
        self.fields['plan'].widget.attrs['onchange']="javascript:Buscar()"
        self.fields['semestre'].widget.attrs['onchange']="javascript:Buscar()"
        self.fields['trabaja_actualmente'].widget.attrs['onchange']="javascript:showContent1()"
        self.fields['carrera'].widget.attrs['onchange']="javascript:Buscar()"
        self.fields['matricula'].widget.attrs['placeholder']="AACCCC"
        self.fields['email'].widget.attrs['readonly'] = "readonly"
        self.fields['matricula'].widget.attrs['readonly'] = "readonly"
        self.fields['municipio'].widget.attrs['onchange'] = "javascript:cambiarLocalidad();"
        self.fields['estado'].widget.attrs['onchange'] = "javascript:cambiarMunicipio();"
        self.fields['municipio'].widget.attrs['disabled'] = True

        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))


        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Datos Personales',
                    'is_active',
                    'nom_alumno',
                    'apellido_paterno',
                    'apellido_materno',
                    Fieldset('Credencial', 'foto', 'firma', id='img'),
                    'curp',
                    'sexo',
                    'edad',
                    'lugar_nac',
                    'fecha_nacimiento',
                    'edo_civil',
                    Fieldset('Datos medicos', 'tipo_sangre', 'alergias', 'enfermedades', HTML("""<div id="div_id_seguro" class="checkbox"> <label for="id_seguro" class=""> <input checked="checked" class="checkboxinput" id="id_seguro" name="seguro" type="checkbox" value="1" onchange="javascript:showContent()">
                    Servicio Medico</label> </div>"""), Div('num_afiliacion', 'servicio_medico', id='div_ServicioMedico')),
                    Fieldset('Domicilio', 'colonia', 'estado', 'municipio', HTML(
                        """<div class="form-group" id="div_id_localidad"> <label class="control-label form-group" for="id_localidad">Localidad</label> <div class="controls "> <select " name="localidad" id="id_localidad" class="select form-control" disabled="True" ><option selected="selected" value="">---------</option></select> </div> </div>"""),
                             'domicilio', 'telefono', 'cp',
                             id='domicilio'),
                     Fieldset('Correo','email')
                ),

                Tab(
                    'Datos Escolares',
                    Fieldset('Procedencia', HTML("""<a data-toggle="modal"
                        data-target="#modalEscuela"
                        id="modal-button"><i class="fa fa-plus-circle"></i></a>"""), 'escuela_procedencia',
                             'anio_egreso', 'promedio_bachiller'),
                    Fieldset('Control Escolar', 'plan', 'semestre', 'matricula','condicionado'),

                    css_class="nav nav-tabs"
                ),
                Tab(
                    'Documentacion y Datos Varios',
                    Fieldset('En caso de emergencia avisar a:', 'contacto_emergencia', 'contacto_domicilio',
                             'contacto_tel'),
                    Fieldset('Datos Familiares',
                             Fieldset('Datos del padre o tutor', 'nombre_tutor', 'domicilio_tutor', 'localidad_tutor',
                                      'telefono_tutor', 'ocupacion_tutor', 'sueldo_mensual', HTML(
                                     """<a class="btn btn-block btn-success" id='id_boton_copiar' onclick="javascript:datacopy()"><i class="fa fa-copy"></i>Copiar datos a la madre</a>""")),
                             Fieldset('Datos de la madre', 'nombre_materno', 'domicilio_madre', 'localidad_madre',
                                      'telefono_madre'),
                             Fieldset('Datos generales', 'trabaja_actualmente',
                                      Div('puesto', 'sueldo_mensual_alumno', id='div_trabajo_estudiante'))),
                    Fieldset('Entrega de documentos', 'acta_nacimiento', 'certificado_bachillerato',
                             'fotografia_titulo', 'otro_documento'),
                    Fieldset('Actividades', 'deporte_practica'),
                    Div('oratoria', 'musica',
                        'teatro', 'declamacion', 'otro_interes'),
                    Fieldset('Transporte', 'transporte', 'transporte_universidad'),

                    css_class="nav nav-tabs"
                ),

                css_class="nav-tabs-custom"
            )

        )

    def clean(self):
        cleaned_data = self.cleaned_data.copy()


        fecha_nacimiento = cleaned_data.pop('fecha_nacimiento', None)
        fecha_actual = timezone.now()

    def save(self, force_insert=False, force_update=False, commit=True):
        entity = super(ReinscripcionAlumnoForm, self).save(commit)
        print('begin'+ entity.is_active.__str__())
        entity.is_active = True
        print("before"+entity.is_active.__str__())
        entity.save()
        return entity


class PlanEstudioForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Guardar'))
    helper.layout = Layout(
        Fieldset('Plan de estudio', 'nom_plan', 'clave_plan','modalidad','duracion','objetivo'),
        Div('materias')
    )

    class Meta:
        model = PlanEstudio
        exclude = ("baja_date_created", "alta_date_created", "is_active")


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupos
        exclude = ("baja_date_created", "alta_date_created", "is_active")


    def __init__(self, *args, **kwargs):
        super(GrupoForm, self).__init__(*args, **kwargs)
        self.fields['cant_alumnos'].widget.attrs['min'] = 0
        self.fields['actual'].widget.attrs['min'] = 0
        self.helper = FormHelper()
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.layout = Layout(
            Fieldset('Grupo', 'clave', 'nombre', 'cant_alumnos', 'semestre', 'actual', 'ciclo_escolar', 'plan')
        )



class GrupoUpdateForm(forms.ModelForm):
    class Meta:
        model = Grupos
        fields = '__all__'



    def __init__(self, *args, **kwargs):
        super(GrupoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['cant_alumnos'].widget.attrs['min'] = 0
        self.fields['actual'].widget.attrs['min'] = 0
        self.helper = FormHelper()
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.layout = Layout(
            Fieldset('General','clave','nombre','cant_alumnos','semestre','actual','ciclo_escolar','plan'
            )
        )


class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        exclude = ("baja_date_created", "alta_date_created", "is_active")

    dia = forms.ChoiceField(choices=DIAS_SELECT,
                             widget=forms.Select(), required=False, label='Dia')
    def __init__(self, *args, **kwargs):
        super(HorarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-group'
        self.fields['materia'].widget.attrs['onchange']="javascript:cambiarProfesores()"
        self.fields['profesores'].widget.attrs['disabled'] = True
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.add_layout(
        Fieldset('Adicionar Horario',
                 'clave_horario',
                 'nombre',
                 'materia',
                 'profesores',
                 'hora_inicio',
                 'minutos_inicio',
                 'hora_termino',
                 'minutos_termino',
                 'dia',
                 'aula',
                 'grupo',


                 ),
    )




class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materias
        exclude = ("baja_date_created", "alta_date_created", "is_active")

    def __init__(self, *args, **kwargs):
        super(MateriaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.add_layout(
        Fieldset('Agregar nueva materia', 'nom_materia','clave','seriacion','creditos','semestre','profesores','hr_docente','hr_independiente','instalacion'
                 ),

    )


class MaestroForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Guardar'))
    helper.layout = Layout(
        Fieldset('Registro de profesor', 'nombre', 'last_name', 'no_expediente', 'email', 'foto')
    )

    class Meta:
        model = Maestros
        exclude = ("baja_date_created", "alta_date_created", "is_active")

    def __init__(self, *args, **kwargs):
        super(MaestroForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))

    def clean_email(self):
        email = self.cleaned_data['email']
        is_insert = self.instance.pk is None
        if is_insert:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError("Existe un usuario con este email por favor cambiarlo")
        else:
            self.fields['email'].widget.attrs['readonly'] = "readonly"
        return email

    def clean_no_expediente(self):
        no_expediente = self.cleaned_data['no_expediente']
        is_insert = self.instance.pk is None
        if is_insert:
            try:
                User.objects.get(no_expediente=no_expediente)
            except User.DoesNotExist:
                return no_expediente
            raise forms.ValidationError("Existe un usuario con este Numero de expediente por favor cambiarlo")
        else:
            self.fields['no_expediente'].widget.attrs['readonly'] = "readonly"
        return no_expediente


class CalificacionForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'box box-success'
    helper.label_class = 'form-group'
    helper.add_input(Submit('submit', 'Guardar'))
    helper.layout = Layout(
        TabHolder(
            Tab('Estudiante', 'matricula', 'semestre', 'plan', 'materia', 'borrado', 'tipoacreditacion', 'actualizado',
                'login'),
            Tab('Calificaciones','final','status_final'),
#'primera', 'status1', 'segunda','status2','tercera','status3','cuarta','status4','quinta','status5','sexta','status6',
            Tab('Revalidacion', 'fecha_revalidacion', 'fecha_modificacion', 'modulo'),
            Tab('Otros', 'claveubicacion', 'id_curso', 'fecha_extraordinario')
        )
    )

    class Meta:
        model = Calificaciones
        fields = '__all__'


class CarreraForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_layout(
        Fieldset('Agregar nueva Carrera', 'nom_carrera', 'clave', 'abreviatura', 'plan_estudio'),

    )

    class Meta:
        model = Carreras
        exclude = ("baja_date_created", "alta_date_created", "is_active")


class CarreraUpdateForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Enviar'))
    helper.add_layout(
        Fieldset('Agregar nueva Carrera', 'nom_carrera', 'clave', 'abreviatura', 'plan_estudio'),

    )


class CicloSemestralForm(forms.ModelForm):
    class Meta:
        model = CicloSemestral
        fields = '__all__'
        exclude = ("baja_date_created", "alta_date_created", "is_active", "periodo", "fecha_inicio_programacion",
                   "fecha_fin_programacion")

        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datepicker ui-widget ui-widget-content date-field'}),
            'fecha_termino': forms.DateInput(
                attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datepicker ui-widget ui-widget-content date-field'}),
        }

    def __init__(self, *args, **kwargs):
        super(CicloSemestralForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.fields['anio'].widget.attrs['min'] = 0
        self.helper.add_input(Submit('submit', 'Guardar'))



MOTIVO_BAJA = (
    ('Voluntaria', 'Voluntaria'),
    ('Reprobación','Reprobación'),
    ('Repetición','Repetición')

)

widget_text_area = forms.CharField(max_length=250, widget=forms.Textarea(
    attrs={'rows': '4', 'cols': '30', 'class': ' form-control'}))

class BajasForm(forms.ModelForm):
    class Meta:
        model = Bajas
        fields = '__all__'
        exclude = ("baja_date_created", "is_active")

    motivo = forms.ChoiceField(choices=MOTIVO_BAJA, widget=forms.Select(), initial='Voluntaria')
    observaciones = CharField(max_length=140, required=False,widget=Textarea(attrs={'rows': 3, 'cols': 33,
                                              'style': 'height: 200px;',
                                              'placeholder':
                                              'Ingrese la observacion'}))
    #matricula=CharField(max_length=17, required=False, widget=TextInput(attrs={'size': '10', 'class': 'form-scontrol'}))

    def __init__(self, *args, **kwargs):
        super(BajasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Aceptar', css_class="btn btn-success"))
        self.helper.layout = Layout(
            Fieldset('Dar baja a estudiante', 'matricula','motivo', 'observaciones')
        )

class BibliotecaForm(forms.ModelForm):
    class Meta:
        model = Biblioteca
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BibliotecaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Aceptar', css_class="btn btn-success"))
        self.helper.layout = Layout(
            Fieldset('Deudas en Biblioteca', 'alumno', 'observacion', 'alta_date_created', 'baja_date_created',
                     'is_active')
        )


class CentroComputoForm(forms.ModelForm):
    class Meta:
        model = CentroComputo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CentroComputoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Aceptar', css_class="btn btn-success"))
        self.helper.layout = Layout(
            Fieldset('Deudas en Centro de Computo', 'alumno', 'observacion', 'alta_date_created', 'baja_date_created',
                     'is_active')
        )


class ContabilidadForm(forms.ModelForm):
    class Meta:
        model = Contabilidad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContabilidadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Aceptar', css_class="btn btn-success"))
        self.helper.layout = Layout(
            Fieldset('Deudas en Contabilidad', 'alumno', 'observacion', 'alta_date_created', 'baja_date_created',
                     'is_active')
        )


class EvaluacionForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Aceptar', css_class='btn btn-primary btn-sm'))
    helper.layout = Layout(
        Fieldset('Agregar evaluacion a estudiante', 'materia', 'alumno', 'calificacion'),
        Button(name='addEval', value='Nueva Calificacion', css_class='btn btn-success'),
    )

    class Meta:
        model = Evaluacion
        fields = '__all__'


widget_text_area = forms.CharField(max_length=250, widget=forms.Textarea(
    attrs={'rows': '4', 'cols': '30', 'class': 'form-control'}))


class EncuestaForm(forms.ModelForm):
    class Meta:
        model = EncuestaEgresados
        exclude = ("baja_date_created", "alta_date_created", "is_active")

    sexo = forms.ChoiceField(choices=GENERO_SELECT,
                             widget=forms.Select(), required=False)

    estado_civil = forms.ChoiceField(choices=Estado_Civil,
                                     widget=forms.Select(), required=False, label='Estado Civil')
    comentarios = widget_text_area

    def __init__(self, *args, **kwargs):
        super(EncuestaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-primary'))
        self.helper.layout = Layout(
            TabHolder(
                Tab('Datos Personales', 'nombre', 'sexo', 'carrera', 'telefono', 'edad', 'correo_electronico',
                    'estado_civil'),
                Tab('Cuestionario 1', 'preg_9', 'porque_preg_9', 'preg_10', 'preg_11', 'preg_12', 'preg_13',
                    ' porque_preg_13 ', 'preg_14', 'porque_preg_14 ', 'preg_15', 'preg_16', 'preg_17', 'preg_18',
                    ' preg_19', 'preg_20'),
                Tab('Cuestionario 2', 'preg_21_1', 'preg_21_2', 'preg_21_3', 'preg_21_4', 'preg_21_5', 'preg_21_6',
                    'preg_21_7', 'preg_21_8', 'preg_21_9', 'preg_21_10', 'preg_22', ' preg_23', 'preg_24', 'preg_25',
                    'preg_26', 'preg_27', 'preg_28', 'porque_preg_28', 'preg_29'),
                Tab('Cuestionario 3', 'preg_30', 'porque_preg_30', 'preg_31_1', 'preg_31_2 ', 'preg_31_3', 'preg_31_4 ',
                    'preg_31_5', 'preg_31_6 ',
                    'preg_31_7 ',
                    'preg_31_8',
                    'preg_31_9',
                    'preg_31_10',
                    'preg_31_11',
                    'porque_preg_31_1 ',
                    'porque_preg_31_2 ',
                    'preg_32 ',
                    'preg_33_1 ',
                    'preg_33_2',
                    'preg_33_3',
                    'preg_33_4',
                    'preg_34_1',
                    'preg_34_2',
                    'preg_34_3',
                    'preg_34_4',
                    'preg_34_5 ',
                    'preg_34_6 ',
                    'preg_34_7 ',
                    'preg_34_8',
                    'preg_34_9',
                    'preg_34_10 ',
                    'preg_34_11',
                    'preg_34_12',
                    'preg_35_1',
                    'preg_35_2 ',
                    'preg_35_3',
                    'preg_35_4',
                    'preg_36',
                    'preg_37',
                    'preg_38_1',
                    'preg_38_2 ',
                    'preg_38_3 ',
                    'preg_38_4',
                    'preg_38_5',
                    'preg_39',
                    ),
                Tab('Cuestionario 4', 'preg_40',
                    'preg_41',
                    'porque_preg_41',
                    'preg_42',
                    'porque_preg_42'),
                Tab('Comentarios Finales', 'comentarios')
            )
        )


class MunicipioForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        'estado', 'nom_municipio', 'is_active'

    )

    class Meta:
        model = Municipios
        fields = '__all__'


class AulaForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        'nom_aula', 'edificio'
    )

    class Meta:
        model = Aulas
        exclude = ("baja_date_created", "is_active")


class EstadoForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        'nom_estado', 'clave', 'is_active'

    )

    class Meta:
        model = Estados
        fields = '__all__'


# listas

class listaAlumnosForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = ('id', 'no_expediente', 'apellido_paterno', 'apellido_materno', 'nom_alumno', 'semestre')


class listaGruposForm(forms.ModelForm):
    class Meta:
        model = Grupos
        fields = '__all__'


class ConsultaAlumnosListForm(forms.Form):
    plan = forms.ModelChoiceField(queryset=mixins.getPlanListado(),
                                  widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    semestre = forms.ModelChoiceField(queryset=mixins.getCicloSemestral(), widget=forms.Select(), required=False)

    expediente = forms.CharField(label='expediente', min_length=9, max_length=9, required=False,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': "No_Expediente", 'class': 'form-control'}))
    nombre = forms.CharField(label='nombre', min_length=9, max_length=9, required=False,
                             widget=forms.TextInput(attrs={'placeholder': "Nombre", 'class': 'form-control'}))
    apellido_paterno = forms.CharField(label='apellido Paterno', min_length=9, max_length=9, required=False,
                                       widget=forms.TextInput(
                                           attrs={'placeholder': "Apellido", 'class': 'form-control'}))
    apellido_materno = forms.CharField(label='apellido Materno', min_length=9, max_length=9, required=False,
                                       widget=forms.TextInput(
                                           attrs={'placeholder': "Apellido", 'class': 'form-control'}))


class ConsultaCicloSemestralListForm(forms.Form):
    clave = forms.CharField(label='Clave', min_length=9, max_length=9, required=False,
                            widget=forms.TextInput(attrs={'placeholder': "2020-01", 'class': 'form-control'}))
    cicloSep = forms.CharField(label='Ciclo SEP', min_length=9, max_length=9, required=False,
                               widget=forms.TextInput(attrs={'placeholder': "1-2", 'class': 'form-control'}))

    anio = forms.CharField(label='Año', min_length=9, max_length=9, required=False,
                           widget=forms.TextInput(attrs={'placeholder': "2020", 'class': 'form-control'}))
    periodo = forms.CharField(label='Periodo', min_length=9, max_length=9, required=False,
                              widget=forms.TextInput(attrs={'placeholder': "1", 'class': 'form-control'}))


class ConsultaExtracurricularListForm(forms.Form):
    clave = forms.CharField(label='Clave Extracurricular', max_length=15, required=False,
                            widget=forms.TextInput(attrs={'placeholder': "2020-01", 'class': 'form-control'}))
    nombre = forms.CharField(label='Nombre', min_length=9, max_length=9, required=False)


class ServicioSocialForm(forms.ModelForm):
    class Meta:
        model = ServicioHoras
        fields = '__all__'

    # alumno = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ServicioSocialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.layout = Layout(
            'alumno', 'proyecto', 'horas', 'is_active'
        )


# class ServicioSocialForm(forms.ModelForm):
#      alumno = forms.ModelChoiceField(queryset=mixins.getEstudiantesPuedenSS(),
#                                   widget=forms.Select(attrs={'class': 'form-control'}), required=True)
#
#      proyecto=forms.ModelChoiceField(queryset=mixins.getEmpresas(),
#                                   widget=forms.Select(attrs={'class': 'form-control'}), required=True)
#
#      horas = forms.CharField(label='Horas', min_length=9, max_length=9, required=False,
#                                widget=forms.TextInput(attrs={'placeholder': "24", 'class': 'form-control'}))
#
#      class Meta:
#         model = ServicioHoras
#         fields = '__all__'


class BecasForm(forms.ModelForm):
    class Meta:
        model = Becas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BecasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.layout = Layout(
            Fieldset('Becas', 'nom_beca', 'tipo_beca', 'alumnos'),
            'restriccion_becas', 'limite_becas_total',
            'restriccion_promedios',
            Fieldset('Promedios', 'promedio_80_84', 'promedio_85_89', 'promedio_90_94', 'promedio_95_100'

                     ),
            'alta_date_created', 'baja_date_created', ' is_active'
        )


class TiposBecasForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        'clave_tipo_beca', 'descripcion', 'is_active'

    )

    class Meta:
        model = TipoBeca
        fields = '__all__'


class EscuelaForm(forms.ModelForm):
    class Meta:
        model = Escuela
        exclude = ("baja_date_created", "alta_date_created", "is_active")

    def __init__(self, *args, **kwargs):
        super(EscuelaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'

class PlanEstudioDetailForm(forms.ModelForm):
    class Meta:
        model = PlanEstudio
        fields = '__all__'

    # alumno = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    def __init__(self, *args, **kwargs):
        super(PlanEstudioDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.layout = Layout(
            Fieldset('Plan de estudio', 'nom_plan','clave_plan','materias')
        )

class SemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = '__all__'
        exclude = ("baja_date_created", "alta_date_created", "is_active")


    def __init__(self, *args, **kwargs):
        super(SemestreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.layout = Layout(
            Fieldset('Agregar semestre','ciclo_semestral'),
            'nombre','clave',

        )


class EntregaDocumentosForm(forms.ModelForm):
    class Meta:
        model = EntregaDocumentos
        fields = '__all__'
        exclude = ("baja_date_created", "alta_date_created", "is_active")

    def __init__(self, *args, **kwargs):
        super(EntregaDocumentosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-group'
        self.helper.layout = Layout(
            Fieldset('Entrega de Documentos', 'ciclo_semestral'),
            'nombre', 'clave',

        )
