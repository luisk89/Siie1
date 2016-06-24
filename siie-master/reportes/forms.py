from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from academica.models import Alumnos

__author__ = 'Luisk'
from django import forms


class InscripcionReporteForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Guardar'))
    helper.layout = Layout(Fieldset(
        'Datos Personales',
        'is_active',
        'nom_alumno',
        'apellido_paterno',
        'apellido_materno',
        )
    )

    class Meta:
        model = Alumnos
        fields = '__all__'
