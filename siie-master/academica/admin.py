from django.contrib import admin

# Register your models here.
from academica.models import Carreras, PlanEstudio, Materias, CicloSemestral, Aulas, Maestros, Horario, Estados, Alumnos, Grupos

admin.site.register(Carreras)
admin.site.register(Alumnos)
admin.site.register(PlanEstudio)
admin.site.register(Materias)
admin.site.register(CicloSemestral)
admin.site.register(Aulas)
admin.site.register(Maestros)
admin.site.register(Horario)
admin.site.register(Estados)
admin.site.register(Grupos)

