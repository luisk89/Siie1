from django.conf.urls import patterns, include, url
from .views import UserDetailView

urlpatterns = patterns(
    '',
    url(r'log-out/$', 'users.views.LogOut', name='logout'),
    url(r'usuario/$', UserDetailView.as_view(), name='user_detail'),
    )