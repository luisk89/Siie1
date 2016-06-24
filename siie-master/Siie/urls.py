from . import views
# from dajaxice.core.Dajaxice import dajaxice_autodiscover
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
# dajaxice_autodiscover()


urlpatterns = patterns('',
                       # Examples:

                       url(r'^academica/', include('academica.urls')),
                       # url(r'^/accounts/login/$', include('allauth.urls', namespace='allauth', app_name='allauth')),
                       url(r'^$', 'Siie.views.login', name="login"),
                       url(r'^Index', login_required(views.Index.as_view()), name="Index"),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^accounts/', include('allauth.urls')),
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^markdown/', include("django_markdown.urls")),
                       url(r'^', include('users.urls', namespace='users')),
                       url(r'^', include('reportes.urls', namespace='reportes')),
                       #url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls'))

                       )

if getattr(settings, "DEBUG", False):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
