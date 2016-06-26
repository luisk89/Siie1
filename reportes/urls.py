from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from wkhtmltopdf.views import PDFTemplateView
from django.conf.urls.static import static

from Siie import settings
from reportes.views import Boleta_Semestral_To_PDF, Calificacion_por_Materia_to_PDF, Inscripcion_To_PDF_Preview,  Inscripcion_To_PDF,CriteriosView, \
    Reinscripcion_To_PDF,Reinscripcion_To_PDF_Preview, CertificadoFinal_To_PDF, Kardex_To_PDF




urlpatterns = [

    url(r'^pdf/(?P<model>\w+)/$', CriteriosView.as_view(), name='evafinal'),
    url(r'^report/repevafinal/$', Calificacion_por_Materia_to_PDF.as_view(), name='reporte-evafinal'),
    url(r'^report/repboleta/$', Boleta_Semestral_To_PDF.as_view()),
    url(r'^report/repinscrip_preview/(?P<pk>[0-9]+)/$', Inscripcion_To_PDF_Preview.as_view()),
    url(r'^report/repinscrip/(?P<pk>[0-9]+)/$', Inscripcion_To_PDF.as_view()),
    url(r'^report/reinscriprep/(?P<pk>[0-9]+)/$', Reinscripcion_To_PDF.as_view()),
    url(r'^report/reinscriprep_preview/(?P<pk>[0-9]+)/$', Reinscripcion_To_PDF_Preview.as_view()),
    url(r'^report/certifinalrep/(?P<pk>[0-9]+)/$', CertificadoFinal_To_PDF.as_view()),
    url(r'^report/kardex/(?P<pk>[0-9]+)/$', Kardex_To_PDF.as_view()),

    url(r'^pdf/$', PDFTemplateView.as_view(template_name='my_template.html',
                                           filename='my_pdf.pdf'), name='pdf'),



    #url(r'^$', TemplateView.as_view(template_name="index3.html"), name='home'),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)