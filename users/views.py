from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import logout
from .models import User
from django.core.mail import EmailMessage
from .forms import UserFormPerfil
from django.views.generic.edit import FormMixin
from django.views.generic import UpdateView
from django.template import RequestContext



# Create your views here.

def send_email(request):

	msg = EmailMessage(subject='Bienvenida',
						from_email = 'rraidel89@gmail.com',
						to=[request.user.email])

	msg.template_name = 'Bienvenido'
	msg.template_content = {
		'usuario' : '<h1>HOLA %s Bienvenido </h1>' % request.user
	}
	msg.send()


#class UserDetailView(FormView):
#    template_name = 'user_detail.html'
#    form_class = EditFormPerfil
#    success_url = reverse_lazy('index')

#    def form_valid(self, form):
#        form.save()
#        messages.success(self.request, 'Su perfil a sido editado.')
#        return super(UserDetailView, self).form_valid(form)

#    def get_context_data(self, **kwargs):
#        context = super(UserDetailView, self).get_context_data(**kwargs)
#        context['object'] = self.request.user
#        return context


class UserDetailView(UpdateView):
	model = User
	form_class = UserFormPerfil
	template_name = 'account/user_detail.html'
	success_url = reverse_lazy('Index')

	def get_object(self, queryset=None):
		return self.request.user

	def form_valid(self, form):
		messages.success(self.request, 'Perfil Editado.')
		return super(UserDetailView, self).form_valid(form)


		return context

def LogOut(request):
	logout(request)
	return redirect('/')
