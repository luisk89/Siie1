from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from django.forms.util import ErrorList
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,MultiField,Div,HTML,Button,Field
from crispy_forms.bootstrap import TabHolder, Tab
from django.contrib.auth import get_user_model
class ExtraDataForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('username' , 'email')

class EditFormPerfil(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name', 'avatar')


    def __init__(self, *args, **kwargs):
        super(EditFormPerfil, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['username'].label = "Usuario"
        self.fields['email'].label = "Correo"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.helper.layout = Layout(
            Fieldset(
                '',
                    Div(
                    HTML("""
                        {% if object.avatar %}
                        <img src="{{object.avatar.url}}" class="avatar img-circle img-thumbnail" alt="avatar">
                        {% endif %}
                    """),
                    Field('avatar'),
                    css_class='col-md-4 col-sm-6 col-xs-12'
                    ),
                    Div(
                        Div(HTML("""
                        <h3>Personal info</h3>
                    """),
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    css_class= 'col-md-8 col-sm-6 col-xs-12 personal-info',
                    ),
                    Div(
                        Div(HTML("""
                        <div class="form-group">
                            <label class="col-md-3 control-label"></label>
                            <div class="col-md-8 col-md-offset-4">
                                  <div class="btn-group">
                                    <input type="submit" name="submit" class="btn btn-primary " id="submit_btn" value="Guardar">
                                  </div>
                                  <div class="btn-group margin-bottom">
                                    <a href="/" class="btn btn-danger" value="Salir" type="button">Salir</a>
                                  </div>
                             </div>
                        </div>
                    """),

                    ),
                        ),
                    css_class= 'col-md-8 col-sm-6 col-xs-12 personal-info',
                    ),
            ),

    )


class UserFormPerfil(forms.ModelForm):

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Guardar'))
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Datos Usuario',
                'username',
                'email',
                'first_name',
                'last_name',
                'avatar'
            ),

        )

    )

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name', 'avatar')
