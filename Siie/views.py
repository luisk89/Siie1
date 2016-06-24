from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView


def login(request):
    return render_to_response('account/login.html', context_instance=RequestContext(request))

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())

class Index (LoginRequiredMixin,TemplateView):
    template_name = 'academica/index.html'