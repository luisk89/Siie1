from django.utils import timezone
import datetime
import json
from django.http.response import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from wkhtmltopdf.views import PDFTemplateView
from academica.models import Alumnos, Grupos, Calificaciones, Materias, PlanEstudio, Carreras, Semestre, CicloSemestral
from reportes.forms import InscripcionReporteForm


class CriteriosView(TemplateView):

    def get_context_data(self, **kwargs):
        cxt = super(CriteriosView, self).get_context_data(**kwargs)
        cxt = {'carreras': Carreras.objects.all(), 'materias': Materias.objects.all(), 'grupos': Grupos.objects.all(),
               'semestres': Semestre.objects.all(),'alumnos':Alumnos.objects.all(),'ciclos':CicloSemestral.objects.all()}
        print('id' + self.kwargs['model'])
        return cxt

    def get_template_names(self):
        model = self.kwargs['model']
        self.model = model
        if model == "boleta":
            self.template_name = "reportes/%s_form.html" % model
        if model == "evafinal":
            self.template_name = "reportes/%s_form.html" % model
        if model=='inscripcion':
            self.template_name="reportes/%s_form.html" % model
        if model=='reinscripcion':
            self.template_name="reportes/%s_form.html" % model
        if model=='certifinal':
            self.template_name="reportes/%s_form.html" % model
        if model=='kardex':
            self.template_name="reportes/%s_form.html" % model

        return self.template_name


class Calificacion_por_Materia_to_PDF(TemplateView):
    template_name = 'reportes/reporte_evafinal_form.html'

    # def datos_evafinal_ajax(request):
    #     if request.is_ajax():
    #
    #         print(request.GET['carrera'])
    #         print(request.GET['materia'])
    #         print(request.GET['ciclo'])
    #         print(request.GET['grupo'])
    #         print(request.GET['semestre'])
    #         retorno=()
    #
    #         return HttpResponse('reportes/reporte_evafinal_form.html',json.dumps(retorno))
    #     else:
    #         return redirect('/')



class Boleta_Semestral_To_PDF(TemplateView):
    template_name = 'reportes/reporte_boleta_form.html'


class Inscripcion_To_PDF_Preview(DetailView):
    template_name = 'reportes/Reporte_Inscripcion.html'
    form_class = InscripcionReporteForm
    model = Alumnos

    def get_context_data(self, **kwargs):
        cxt = super(Inscripcion_To_PDF_Preview, self).get_context_data(**kwargs)
        hoy = datetime.datetime.now()
        hoy = hoy.strftime('%d %b, %Y')
        alumno=Alumnos.objects.get(id=self.kwargs['pk'])
        fecha_ins=alumno.alta_date_created.strftime('%Y-%m-%d')
        cxt = {'hoy': hoy,'fecha_insc':fecha_ins,'object':alumno}

        return cxt

class Inscripcion_To_PDF(PDFTemplateView):
    template_name = 'reportes/Reporte_Inscripcion.html'
    form_class = InscripcionReporteForm
    model = Alumnos
    cmd_options = {
        'page-size': 'A3',
        'margin-top': 15,
        'margin-right': 1,
        'margin-bottom': 1,
        'margin-left': 1,
    }
    def get_context_data(self, **kwargs):
        cxt = super(Inscripcion_To_PDF, self).get_context_data(**kwargs)
        hoy = datetime.datetime.now()
        hoy = hoy.strftime('%d %b, %Y')
        alumno=Alumnos.objects.get(id=self.kwargs['pk'])
        fecha_ins=alumno.alta_date_created.strftime('%Y-%m-%d')
        name = alumno.matricula
        self.filename='Inscripcion_'+name
        cxt = {'hoy': hoy,'fecha_insc':fecha_ins,'object':alumno}

        return cxt


class Reinscripcion_To_PDF_Preview(DetailView):
    template_name = 'reportes/reporte_reinscripcion.html'
    form_class = InscripcionReporteForm
    model = Alumnos

    def get_context_data(self, **kwargs):
        cxt = super(Reinscripcion_To_PDF_Preview, self).get_context_data(**kwargs)
        hoy = datetime.datetime.now()
        hoy = hoy.strftime('%d %b, %Y')
        alumno=Alumnos.objects.get(id=self.kwargs['pk'])
        fecha_ins=alumno.alta_date_created.strftime('%Y-%m-%d')
        cxt = {'hoy': hoy,'fecha_insc':fecha_ins,'object':alumno}

        return cxt

class Reinscripcion_To_PDF(PDFTemplateView):
    template_name = 'reportes/reporte_reinscripcion.html'
    form_class = InscripcionReporteForm
    model = Alumnos
    cmd_options = {
        'page-size': 'A3',
        'margin-top': 15,
        'margin-right': 1,
        'margin-bottom': 1,
        'margin-left': 1,
    }

    def get_context_data(self, **kwargs):
        cxt = super(Reinscripcion_To_PDF, self).get_context_data(**kwargs)
        hoy = datetime.datetime.now()
        hoy = hoy.strftime('%d %b, %Y')
        alumno=Alumnos.objects.get(id=self.kwargs['pk'])
        fecha_ins=alumno.alta_date_created.strftime('%y-%m-%d')
        name = alumno.matricula
        self.filename='Reinscripcion'+name
        cxt = {'hoy': hoy,'fecha_insc':fecha_ins,'object':alumno}

        return cxt

class CertificadoFinal_To_PDF(TemplateView):
    template_name = 'reportes/reporte_certificado_final.html'
    #
    def get_context_data(self, **kwargs):
        cxt = super(CertificadoFinal_To_PDF, self).get_context_data(**kwargs)
        hoy = datetime.datetime.now()
        hoy = hoy.strftime('%d %b, %Y')
        alumno=Alumnos.objects.get(id=self.kwargs['pk'])
        calificaciones=Calificaciones.objects.filter(matricula=alumno.matricula)

        cxt = {'hoy': hoy,'var':'hola mundo','object':alumno,'calificaciones':calificaciones}

        return cxt

class Kardex_To_PDF(TemplateView):
    template_name = 'reportes/reporte_kardex.html'

    #
    def get_context_data(self, **kwargs):
        cxt = super(Kardex_To_PDF, self).get_context_data(**kwargs)
        hoy = datetime.datetime.now()
        anio=hoy.year
        hoy = hoy.strftime('%d %b, %Y')
        alumno=Alumnos.objects.get(id=self.kwargs['pk'])
        calificaciones=Calificaciones.objects.filter(matricula=alumno.matricula)

        cxt = {'hoy': hoy,'var':'hola mundo','object':alumno,'calificaciones':calificaciones,'anio':anio}

        return cxt