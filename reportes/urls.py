from django.conf.urls import patterns, include, url
from wkhtmltopdf.views import PDFTemplateView
from reportes.views import Boleta_Semestral_To_PDF, Calificacion_por_Materia_to_PDF, Inscripcion_To_PDF,CriteriosView, \
    Reinscripcion_To_PDF, CertificadoFinal_To_PDF, Kardex_To_PDF

urlpatterns = patterns('',
                       url(r'^pdf/(?P<model>\w+)/$', CriteriosView.as_view(), name='evafinal'),
                       url(r'^report/repevafinal/$', Calificacion_por_Materia_to_PDF.as_view(), name='reporte-evafinal'),
                       url(r'^report/repboleta/$', Boleta_Semestral_To_PDF.as_view()),
                        url(r'^report/repinscrip/(?P<pk>[0-9]+)/$', Inscripcion_To_PDF.as_view()),
                       url(r'^report/reinscriprep/(?P<pk>[0-9]+)/$', Reinscripcion_To_PDF.as_view()),
                        url(r'^report/certifinalrep/(?P<pk>[0-9]+)/$', CertificadoFinal_To_PDF.as_view()),
                       url(r'^report/kardex/(?P<pk>[0-9]+)/$', Kardex_To_PDF.as_view()),
                       )
