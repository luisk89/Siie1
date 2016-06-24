# -*- encoding: utf-8 -*-
import datetime
from django.contrib.admin import widgets
from django.db.models.fields import DateField
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
    Carreras, CicloSemestral, Bajas, Evaluacion, EncuestaEgresados, Aulas, Municipios, \
    Estados, Calificaciones, ServicioHoras, Becas, TipoBeca, Escuela, Biblioteca, Contabilidad, CentroComputo, Semestre
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
    ('3', 'Equivalencia')
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
hoy = datetime.datetime.now()
hoy = hoy.strftime('%Y-%m-%d')
style_numeric = 'ui-widget ui-widget-content numeric-field'


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
    promedio_bachiller=forms.FloatField(label='Promedio', initial=0.0, widget=forms.TextInput(attrs={'class':style_numeric}), required=False)
    curp=forms.CharField(max_length=18,required=False)
    #semestre = forms.ChoiceField(choices=mixins.getCicloSemestral(),widget=forms.Select(attrs={'class': 'form-control'}), required=False,initial=mixins.getSemestreActive())


    def __init__(self, *args, **kwargs):
        super(AlumnosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['edad'].widget.attrs['min'] = 1
        self.fields['sueldo_mensual'].widget.attrs['min'] = 0
        self.fields['sueldo_mensual_alumno'].widget.attrs['min'] = 0
        self.fields['matricula'].widget.attrs['onfocus']="javascript:Buscar()"
        self.fields['plan'].widget.attrs['onchange']="javascript:Buscar()"
        self.fields['semestre'].widget.attrs['onchange']="javascript:Buscar()"
        self.fields['trabaja_actualmente'].widget.attrs['onchange']="javascript:showContent1()"

        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))


        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Datos Personales',
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
                    Fieldset('Domicilio', 'colonia', 'localidad', 'municipio', 'domicilio', 'telefono', 'cp', 'email',
                             id='domicilio')
                ),

                Tab(
                    'Datos Escolares',
                    Fieldset('Procedencia', HTML("""<a data-toggle="modal"
                        data-target="#modalEscuela"
                        id="modal-button"><i class="fa fa-plus-circle"></i></a>"""), 'escuela_procedencia',
                             'anio_egreso', 'promedio_bachiller'),
                    Fieldset('Control Escolar', HTML("""<a data-toggle="modal"
                        data-target="#modalPlan"
                        id="modal-button"><i class="fa fa-plus-circle"></i></a>"""), 'plan', 'semestre', 'matricula',
                             'condicionado'),
                    # HTML("""<a data-toggle="modal"
                    #     data-target="#modalGrupo"
                    #     id="modal-button"><i class="fa fa-plus-circle"></i></a>"""),
                    #          'grupo', 'is_active'
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
                    Fieldset('Actividades', 'deporte_practica', 'credencial'),
                    Div('oratoria', 'musica',
                        'teatro', 'declamacion', 'otro_interes'),
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
            pass
        return email

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
    promedio_bachiller=forms.FloatField(label='Promedio', initial=0.0, widget=forms.TextInput(attrs={'class':style_numeric}), required=False)



    curp=forms.CharField(max_length=18,required=False)


    def __init__(self, *args, **kwargs):
        super(ReinscripcionAlumnoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['edad'].widget.attrs['min'] = 1
        self.fields['sueldo_mensual'].widget.attrs['min'] = 0
        self.fields['sueldo_mensual_alumno'].widget.attrs['min'] = 0
        self.fields['is_active'].widget = forms.HiddenInput()
        self.fields['matricula'].widget.attrs['onfocus']="javascript:Buscar()"
        self.fields['plan'].widget.attrs['onchange']="javascript:Buscar()"
        self.fields['semestre'].widget.attrs['onchange']="javascript:Buscar()"
        self.fields['trabaja_actualmente'].widget.attrs['onchange']="javascript:showContent1()"

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
                    Fieldset('Domicilio', 'colonia', 'localidad', 'municipio', 'domicilio', 'telefono', 'cp', 'email',
                             id='domicilio')
                ),

                Tab(
                    'Datos Escolares',
                    Fieldset('Procedencia', HTML("""<a data-toggle="modal"
                        data-target="#modalEscuela"
                        id="modal-button"><i class="fa fa-plus-circle"></i></a>"""), 'escuela_procedencia',
                             'anio_egreso', 'promedio_bachiller'),
                    Fieldset('Control Escolar', HTML("""<a data-toggle="modal"
                        data-target="#modalPlan"
                        id="modal-button"><i class="fa fa-plus-circle"></i></a>"""), 'plan', 'semestre', 'matricula',
                             'condicionado'),

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
                    Fieldset('Actividades', 'deporte_practica', 'credencial'),
                    Div('oratoria', 'musica',
                        'teatro', 'declamacion', 'otro_interes'),
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
        'nom_plan',
        'clave_plan',
        'materias',
        'is_active',
    )

    class Meta:
        model = PlanEstudio
        fields = '__all__'


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupos
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(GrupoForm, self).__init__(*args, **kwargs)
        self.fields['cant_alumnos'].widget.attrs['min'] = 0
        self.fields['actual'].widget.attrs['min'] = 0
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.layout = Layout(
            Fieldset('General','clave', 'nombre', 'cant_alumnos', 'semestre', 'actual', 'ciclo_escolar','horarios', 'plan', 'materias')
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
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.layout = Layout(
            Fieldset('General','clave','nombre','cant_alumnos','semestre','actual','ciclo_escolar','plan','materias','horarios'
            )
        )


class HorarioForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Guardar'))
    helper.layout = Layout(
        Fieldset('Adicionar Horario',
                 'clave_horario',
                 'nombre',
                 'hora_inicio',
                 'hora_termino',
                 'minutos_inicio',
                 'minutos_termino',
                 'aula',
                 'profesores',
                 'is_active',
                 'grupos'
                 )
    )

    class Meta:
        model = Horario
        fields = '__all__'


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materias
        exclude = ("baja_date_created", "alta_date_created", "is_active")

    def __init__(self, *args, **kwargs):
        super(MateriaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.add_layout(
        Fieldset('Agregar nueva materia', 'nom_materia','clave','seriacion','creditos','semestre'
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
        fields = '__all__'


class CalificacionForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'box box-success'
    helper.label_class = 'form-group'
    helper.add_input(Submit('submit', 'Guardar'))
    helper.layout = Layout(
        TabHolder(
            Tab('Estudiante', 'matricula', 'semestre', 'plan', 'materia', 'borrado', 'tipoacreditacion', 'actualizado',
                'login'),
            Tab('Calificaciones', 'primera', 'status1', 'segunda','status2','tercera','status3','cuarta','status4','quinta','status5','sexta','status6','final','status_final'),

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
        fields = '__all__'


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
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datepicker ui-widget ui-widget-content date-field'}),
            'fecha_termino': forms.DateInput(
                attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datepicker ui-widget ui-widget-content date-field'}),
            'fecha_inicio_programacion': forms.DateInput(
                attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datepicker ui-widget ui-widget-content date-field'}),
            'fecha_fin_programacion': forms.DateInput(
                attrs={'placeholder': 'dd/mm/aaaa', 'class': 'datepicker ui-widget ui-widget-content date-field'}),

        }

    def __init__(self, *args, **kwargs):
        super(CicloSemestralForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.fields['anio'].widget.attrs['min'] = 0
        self.fields['anio'].widget.attrs['placeholder'] = '1989'
        self.helper.add_input(Submit('submit', 'Guardar'))

        self.helper.layout = Layout(
            Fieldset('Ciclo Semestral','clave', 'ciclo_sep', 'anio', 'periodo', 'fecha_inicio', 'fecha_termino','fecha_inicio_programacion', 'fecha_fin_programacion', 'vigente')

        )


MOTIVO_BAJA = (
    ('Voluntaria', 'Voluntaria'),
    ('Reprobación','Reprobación'),
    ('Repetición','Repetición')

)


class BajasForm(forms.ModelForm):
    class Meta:
        model = Bajas
        fields = '__all__'
        exclude = ("baja_date_created", "is_active")

    motivo = forms.ChoiceField(choices=MOTIVO_BAJA, widget=forms.Select(), initial='Voluntaria')


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
        'nom_aula', 'edificio', 'is_active'
    )

    class Meta:
        model = Aulas
        fields = '__all__'


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

class SemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = '__all__'
        exclude=('alta_date_created','baja_date_created','is_active')


    def __init__(self, *args, **kwargs):
        super(SemestreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'box box-success'
        self.helper.label_class = 'form-group'
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.layout = Layout(
            Fieldset('Agregar Semestre','ciclo_semestral', 'clave')
        )
