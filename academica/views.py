from builtins import print
from django.contrib.auth import get_user_model

import json
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.contrib import messages
from academica.util import LoggedInMixin
from django.contrib.auth.models import Group
from django.utils.translation import activate
from academica.forms import AlumnosForm, PlanEstudioForm, ExtraCurricularesForm, GrupoForm, HorarioForm, MaestroForm, \
    CalificacionForm, CarreraForm, CicloSemestralForm, BajasForm, MateriaForm, CarreraUpdateForm, EncuestaForm, \
    ConsultaAlumnosListForm, ConsultaCicloSemestralListForm, MunicipioForm, EstadoForm, AulaForm, \
    ConsultaExtracurricularListForm, \
    ServicioSocialForm, BecasForm, TiposBecasForm, EscuelaForm, BibliotecaForm, CentroComputoForm, ContabilidadForm, \
    ReinscripcionAlumnoForm, GrupoUpdateForm, listaGruposForm, PlanEstudioDetailForm

activate('es')
# Create your views here.
from academica.models import Alumnos, PlanEstudio, Extracurriculares, Grupos, Horario, Maestros, Materias, \
    AlumnoCalificacion, Carreras, Bajas, Evaluacion, EncuestaEgresados, AlumnoPrevio, Aulas, \
    Municipios, Estados, Calificaciones, ServicioHoras, Becas, TipoBeca, Escuela, Biblioteca, CentroComputo, \
    Contabilidad, Semestre, Localidad


class AlumnoCreate(LoggedInMixin, CreateView):
    template_name = 'academica/alumnos/alumnos_form.html'
    model = Alumnos
    fields = '__all__'
    form_class = AlumnosForm
    success_url = reverse_lazy('list-alumno')

    def get_context_data(self, **kwargs):
        context = super(AlumnoCreate, self).get_context_data(**kwargs)
        context['form_extra'] = ExtraCurricularesForm
        context['form_plan'] = PlanEstudioForm
        context['form_grupo'] = GrupoForm
        context['form_escuela'] = EscuelaForm
        if Semestre.objects.filter(vigente=True):
            semestre = Semestre.objects.filter(vigente=True).get()
            context['semestre'] = semestre
        return context

    def form_valid(self, form):
        username = form.cleaned_data['nom_alumno']
        email = form.cleaned_data['email']
        nombre = form.cleaned_data['nom_alumno']
        apellido_paterno = form.cleaned_data['apellido_paterno']
        avatar = form.cleaned_data['foto']
        matricula = form.cleaned_data['matricula']

        # poniendo como usuario la primeraletra del nombre y el apellido->Ej. rrosal
        usuario = matricula

        # en el formulario esta la validacion para el username y el email (el user name que se crea es el nombre del alumno eso tenemos que cambiarlo, hacer una mescla nombre mas apellido o algo asi)
        user = get_user_model().objects.create_user(usuario, email, avatar=avatar, first_name=nombre,
                                                    last_name=apellido_paterno, no_expediente=matricula)
        user.set_password(usuario)
        g = Group.objects.get(name='Estudiante')
        g.user_set.add(user)
        user.save()
        messages.success(self.request, 'Alumno Creado Correctamente')
        messages.success(self.request, 'Usuario Creado Correctamente')
        messages.success(self.request, 'Usuario:  ' + usuario + '  Password:  ' + usuario)

        return super(AlumnoCreate, self).form_valid(form)

    def buscar_exp_ajax(request):
        if request.is_ajax():

            if request.GET['carrera'] and Carreras.objects.filter(clave=request.GET['carrera']).exists():
                carrera = Carreras.objects.filter(clave=request.GET['carrera']).get().id
            else:
                carrera = "CCC"

            if request.GET['anio']:
                anio = request.GET['anio']
            else:
                anio = "AAAA"

            consect = Alumnos.objects.all().count() + 1


            retorno = (anio + carrera.__str__()+ consect.__str__())

            return HttpResponse(json.dumps(retorno))
        else:
            return redirect('/')

class AlumnoUpdate(LoggedInMixin, UpdateView):
    model = Alumnos
    fields = '__all__'
    template_name = 'academica/alumnos/alumnos_form.html'
    form_class = AlumnosForm

    def get_context_data(self, **kwargs):
        context = super(AlumnoUpdate, self).get_context_data(**kwargs)
        context['form_extra'] = ExtraCurricularesForm
        context['form_plan'] = PlanEstudioForm
        context['form_grupo'] = GrupoForm
        context['form_escuela'] = EscuelaForm

        return context


class AlumnoReins(LoggedInMixin, UpdateView):
    model = Alumnos
    fields = '__all__'
    template_name = 'academica/alumnos/alumnos_re_form.html'
    form_class = ReinscripcionAlumnoForm

    def get_context_data(self, **kwargs):
        context = super(AlumnoReins, self).get_context_data(**kwargs)
        context['form_extra'] = ExtraCurricularesForm
        context['form_plan'] = PlanEstudioForm
        context['form_grupo'] = GrupoForm
        context['form_escuela'] = EscuelaForm

        return context


class AlumnoDelete(LoggedInMixin, DeleteView):
    model = Alumnos
    success_url = reverse_lazy('alumno-list')


class AlumnoList(LoggedInMixin, ListView):
    model = Alumnos
    template_name = 'academica/alumnos/alumnos_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(AlumnoList, self).get_context_data(**kwargs)
        ctx['lista_todos'] = Alumnos.objects.all()
        ctx['search_form'] = ConsultaAlumnosListForm
        return ctx


class ReinscripcionList(LoggedInMixin, ListView):
    model = Alumnos
    template_name = 'academica/alumnos/alumnos_re.html'
    success_url = reverse_lazy('alumno-re')

    def get_queryset(self):
        # para listar estudiantes q se pueden reinscribir
        # verificar q sea baja por voluntario,
        # verificar q no debe nada en biblioteca,contabilidad o centro de computo,
        #
        result = []
        alumnos = Alumnos.objects.filter(is_active=False).all()
        bajas = Bajas.objects.select_related('alumno').filter(motivo="Voluntaria").all()
        for b in bajas:
            if not b.alumno.is_deuda:
                result.append(b.alumno)
            print(b.alumno.is_deuda)
        return result

    def get_context_data(self, **kwargs):
        ctx = super(ReinscripcionList, self).get_context_data(**kwargs)
        ctx['alumno_list'] = Alumnos.objects.all()
        ctx['search_form'] = ConsultaAlumnosListForm
        return ctx

    def AlumnoAjax(request):

        if request.is_ajax():
            # alumnosReturn=Alumnos.objects.filter(Q(nom_alumno__contains=request.GET['nombre']) | Q(apellido_paterno__contains=request.GET['apellidoP'])| Q(apellido_materno__contains=request.GET['apellidoM'])|Q(semestre__id__contains=request.GET['semestre'])|Q(no_expediente__contains=request.GET['expediente'])).all()
            print(request.GET['semestre'])

            alumnosReturn = Alumnos.objects.filter(nom_alumno__contains=request.GET['nombre']).filter(
                apellido_paterno__contains=request.GET['apellidoP']).filter(
                apellido_materno__contains=request.GET['apellidoM']).filter(
                semestre__id__contains=request.GET['semestre']).filter(
                no_expediente__contains=request.GET['expediente']).filter(plan__id__contains=request.GET['plan'])
            retorno = []
            for alumno in alumnosReturn:
                retorno.append({'id': alumno.id, 'nombre': alumno.nom_alumno, 'apellidoP': alumno.apellido_paterno,
                                'apellidoM': alumno.apellido_materno, 'expediente': alumno.no_expediente,
                                'semestre': alumno.semestre.clave})

            return HttpResponse(json.dumps(retorno))
        else:
            return redirect('/')


class PlanCreate(LoggedInMixin, CreateView):
    model = PlanEstudio
    fields = '__all__'
    template_name = 'academica/planEstudio/planEstudio_form.html'
    form_class = PlanEstudioForm
    success_url = 'planEstudio/list'

    def get_context_data(self, **kwargs):
        context = super(PlanCreate, self).get_context_data(**kwargs)
        context['form_plan'] = PlanEstudioForm
        context['form'] = MateriaForm
        context['form_carrera'] = CarreraForm
        return context


class PlanUpdate(LoggedInMixin, UpdateView):
    model = PlanEstudio
    fields = '__all__'
    template_name = 'academica/planEstudio/planEstudio_form.html'
    form_class = PlanEstudioForm


class PlanEstudioList(LoggedInMixin, ListView):
    model = PlanEstudio
    template_name = 'academica/planEstudio/planEstudio_list.html'

    def get_context_data(self, **kwargs):
        context = super(PlanEstudioList, self).get_context_data(**kwargs)
        context['form_plan'] = PlanEstudioForm
        return context

    def get_plan_by_alumno(request):
        user=request.user
        plan=Alumnos.objects.get(matricula=user.no_expediente).plan

        return render_to_response('planEstudio/detail/'+plan.id+'/')

class PlanEstudioDetail(LoggedInMixin,DetailView):
    model = PlanEstudio
    template_name = 'academica/planEstudio/planEstudio_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PlanEstudioDetail, self).get_context_data(**kwargs)
        context['form_plan'] = PlanEstudioDetailForm
        return context

class CarreraCreate(LoggedInMixin, CreateView):
    model = Carreras
    template_name = 'academica/carrera/carrera_form.html'
    form_class = CarreraForm

    def get_context_data(self, **kwargs):
        context = super(CarreraCreate, self).get_context_data(**kwargs)
        context['form_plan'] = PlanEstudioForm
        return context


class CarreraUpdate(LoggedInMixin, UpdateView):
    model = Carreras
    fields = '__all__'
    template_name = 'academica/carrera/carrera_update_form.html'
    form_class = CarreraUpdateForm


class CarreraList(LoggedInMixin, ListView):
    model = Carreras
    template_name = 'academica/carrera/carrera_list.html'

    def get_context_data(self, **kwargs):
        context = super(CarreraList, self).get_context_data(**kwargs)
        context['form_materia'] = MateriaForm
        context['form_plan'] = PlanEstudioForm
        context['form_carrera'] = CarreraForm
        return context


class GrupoCreate(LoggedInMixin, CreateView):
    model = Grupos
    fields = '__all__'
    template_name = 'academica/grupo/grupo_form.html'
    form_class = GrupoForm

    def get_context_data(self, **kwargs):
        cxt = super(GrupoCreate, self).get_context_data(**kwargs)
        cxt['form_grupo'] = GrupoForm
        if Semestre.objects.filter(is_active=True):
            cxt['semestre'] = Semestre.objects.filter(is_active=True).get()
        return cxt


class GruposList(LoggedInMixin, ListView):
    model = Grupos
    template_name = 'academica/grupo/grupos_list.html'

    def get_context_data(self, **kwargs):
        cxt = super(GruposList, self).get_context_data(**kwargs)
        cxt['form_grupo'] = GrupoForm
        return cxt


class GrupoUpdate(LoggedInMixin, UpdateView):
    model = Grupos
    fields = '__all__'
    template_name = 'academica/grupo/grupo_update_form.html'
    form_class = GrupoUpdateForm

    def get_context_data(self, **kwargs):
        context = super(GrupoUpdate, self).get_context_data(**kwargs)
        context['form_grupoupdate'] = GrupoUpdateForm
        return context


class HorarioCreate(LoggedInMixin, CreateView):
    model = Horario
    fields = '__all__'
    template_name = 'academica/horario/horario_form.html'
    form_class = HorarioForm


class HorarioUpdate(LoggedInMixin, UpdateView):
    model = Horario
    fields = '__all__'
    template_name = 'academica/horario/horario_update_form.html'
    form_class = HorarioForm


class HorarioList(LoggedInMixin, ListView):
    model = Horario
    template_name = 'academica/horario/horario_list.html'

    def get_context_data(self, **kwargs):
        context = super(HorarioList, self).get_context_data(**kwargs)
        context['form'] = HorarioForm

        return context

    def get_horarios_profesor(request):
        user = request.user
        no_expediente = user.no_expediente
        print(Horario.objects.get(id=2).profesores)
        print(user)
        horarios=Horario.objects.filter(profesores__no_expediente=user.no_expediente).all()
        print(Horario.objects.filter(profesores__no_expediente=user.no_expediente).all())
        return render_to_response('academica/horario/mis_horarios.html', {'list':horarios})

    def get_horarios_alumno(request):

        user = request.user
        print(user)
        no_expediente = user.no_expediente

        alumnoNombre = Alumnos.objects.get(matricula=no_expediente)

        if (Grupos.objects.filter(clave=alumnoNombre.grupo.clave).all()):
            group = Grupos.objects.filter(id=alumnoNombre.grupo.id).get()
            horarios = Horario.objects.filter(grupo=group).all()

        return render_to_response('academica/horario/mis_horarios.html', {'list':horarios})


class MateriaCreate(LoggedInMixin, CreateView):
    model = Materias
    template_name = 'academica/materia/materia_form.html'
    form_class = MateriaForm

    def get_context_data(self, **kwargs):
        context = super(MateriaCreate, self).get_context_data(**kwargs)
        context['form_materia'] = MateriaForm
        return context


class MateriaList(LoggedInMixin, ListView):
    model = Materias
    template_name = 'academica/materia/materia_list.html'

    def get_context_data(self, **kwargs):
        context = super(MateriaList, self).get_context_data(**kwargs)
        context['form_materia'] = MateriaForm
        return context


class MaestroCreate(LoggedInMixin, CreateView):
    model = Maestros
    fields = '__all__'
    template_name = 'academica/maestro/maestro_form.html'
    form_class = MaestroForm


    def form_valid(self, form):
        username = form.cleaned_data['no_expediente']
        email = form.cleaned_data['email']
        nombre = form.cleaned_data['nombre']
        apellido = form.cleaned_data['last_name']
        avatar = form.cleaned_data['foto']
        no_expediente = form.cleaned_data['no_expediente']

        # poniendo como usuario la primeraletra del nombre y el apellido->Ej. rrosal
        usuario = username
        password = username

        # en el formulario esta la validacion para el username y el email (el user name que se crea es el nombre del alumno eso tenemos que cambiarlo, hacer una mescla nombre mas apellido o algo asi)
        user = get_user_model().objects.create_user(usuario, email, avatar=avatar, first_name=nombre,
                                                    last_name=apellido, no_expediente=no_expediente)
        user.set_password(usuario)
        g = Group.objects.get(name='Maestro')
        g.user_set.add(user)
        user.save()
        messages.success(self.request, 'Maestro Creado Correctamente')
        messages.success(self.request, 'Usuario Creado Correctamente')
        messages.success(self.request, 'Usuario:  ' + usuario + '  Password:  ' + password)

        return super(MaestroCreate, self).form_valid(form)

class MaestroList(LoggedInMixin, ListView):
    model = Maestros
    template_name = 'academica/maestro/maestro_list.html'

    def get_context_data(self, **kwargs):
        context = super(MaestroList, self).get_context_data(**kwargs)
        context['form'] = MaestroForm
        return context


class CalificacionCreate(LoggedInMixin, CreateView):
    model = Calificaciones
    fields = '__all__'
    template_name = 'academica/calificacion/calificacion_form.html'
    form_class = CalificacionForm
    success_url = 'calificacion/list'

    def get_context_data(self, **kwargs):
        context = super(CalificacionCreate, self).get_context_data(**kwargs)
        context['form_calificacion'] = CalificacionForm
        return context


class CalificacionList(LoggedInMixin, ListView):
    model = Calificaciones
    template_name = 'academica/calificacion/calificacion_list.html'

    def get_context_data(self, **kwargs):
        context = super(CalificacionList, self).get_context_data(**kwargs)
        context['form_calificacion'] = CalificacionForm
        context['list_calificacion'] = Calificaciones.objects.all()
        print(Calificaciones.objects.all())
        context['list_alumno'] = Alumnos.objects.filter(is_active=True)
        return context

    def get_calificacionesbyAlumno(request,alumno):
        user = request.user

        alumnoNombre = Alumnos.objects.get(id=alumno)
        list = Calificaciones.objects.filter(matricula=alumnoNombre.matricula)

        return render_to_response('academica/calificacion/calificacion_by_alumno.html',
                                  {'listado': list, 'alumno': alumnoNombre, 'user': user})

    def get_my_calificaciones(request):
        user = request.user
        no_expediente = user.no_expediente
        alumnoNombre = Alumnos.objects.get(matricula=no_expediente)
        list = Calificaciones.objects.filter(matricula=no_expediente)
        return render_to_response('academica/calificacion/mis_calificaciones.html',
                                  {'listado': list, 'alumno': alumnoNombre, 'user': user})


class CalificacionesUpdate(LoggedInMixin, UpdateView):
    model = Calificaciones
    fields = '__all__'
    template_name = 'academica/calificacion/calificacion_detail_form.html'
    form_class = CalificacionForm

class CalificacionesDetail(LoggedInMixin, DetailView):
    model = Calificaciones
    fields = '__all__'
    template_name = 'academica/calificacion/calificacion_update_form.html'
    form_class = CalificacionForm

class CicloSemestralCreate(LoggedInMixin, CreateView):
    model = Semestre
    template_name = 'academica/semestre/ciclosemestral_form.html'
    form_class = CicloSemestralForm

    def form_valid(self, form):
        semestre = form.cleaned_data['vigente']
        if semestre:
            semestresActivos = Semestre.objects.filter(is_active=True)
            if semestresActivos:
                messages.error(self.request, message='Ya hay un semestre activo en el sistema')
                # impedir q inserte el semestre
            else:
                form.save()

        return super(CicloSemestralCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CicloSemestralCreate, self).get_context_data(**kwargs)
        context['form_semestre'] = CicloSemestralForm
        return context


class CicloSemestralUpdate(LoggedInMixin, UpdateView):
    model = Semestre
    fields = '__all__'
    template_name = 'academica/semestre/ciclosemestralUpdate.html'
    form_class = CicloSemestralForm


class CicloSemestralList(LoggedInMixin, ListView):
    model = Semestre
    template_name = 'academica/semestre/ciclosemestral_list.html'

    def get_context_data(self, **kwargs):
        context = super(CicloSemestralList, self).get_context_data(**kwargs)
        context['search_form'] = ConsultaCicloSemestralListForm
        context['form_semestre'] = CicloSemestralForm
        ciclo_activo = False
        for i in Semestre.objects.all():
            if i.vigente:
                ciclo_activo = i
                print("semestre" + ciclo_activo.clave)

        context['semestre'] = ciclo_activo
        return context

    def SemestreAjax(request):

        if request.is_ajax():
            # alumnosReturn=Alumnos.objects.filter(Q(nom_alumno__contains=request.GET['nombre']) | Q(apellido_paterno__contains=request.GET['apellidoP'])| Q(apellido_materno__contains=request.GET['apellidoM'])|Q(semestre__id__contains=request.GET['semestre'])|Q(no_expediente__contains=request.GET['expediente'])).all()

            semestres = Semestre.objects.filter(clave__contains=request.GET['clave']).filter(
                ciclo_sep__contains=request.GET['ciclo']).filter(
                anio__contains=request.GET['anio']).filter(
                periodo__contains=request.GET['periodo'])

            retorno = []
            for s in semestres:
                retorno.append({'clave': s.clave, 'ciclo': s.ciclo_sep, 'anio': s.anio, 'periodo': s.periodo,
                                'fecha_inicio': s.fecha_inicio, 'fecha_fin': s.fecha_termino, 'vigente': s.vigente})

            return HttpResponse(json.dumps(retorno))
        else:
            return redirect('/')


class ExtracurricularesCreate(LoggedInMixin, CreateView):
    model = Extracurriculares
    form_class = ExtraCurricularesForm

    def get_context_data(self, **kwargs):
        context = super(ExtracurricularesCreate, self).get_context_data(**kwargs)
        context['form_extra'] = ExtraCurricularesForm
        return context


class ExtracurricularList(LoggedInMixin, ListView):
    model = Extracurriculares
    template_name = 'academica/alumnos/extracurriculares_list.html'

    def get_context_data(self, **kwargs):
        context = super(ExtracurricularList, self).get_context_data(**kwargs)
        context['extra_list'] = Extracurriculares.objects.all()
        context['form_extra'] = ExtraCurricularesForm
        context['form_search_extra'] = ConsultaExtracurricularListForm
        return context

    def ExtracurricularAjax(request):
        if request.is_ajax():

            ExtraReturn = Extracurriculares.objects.filter(clave__contains=request.GET['clave']).filter(
                nom_materia__contains=request.GET['nombre'])
            retorno = []
            for ex in ExtraReturn:
                retorno.append({'nombre': ex.nom_materia, 'clave': ex.clave})

            return HttpResponse(json.dumps(retorno))
        else:
            return redirect('/')


class BajaCreate(LoggedInMixin, CreateView):
    model = Bajas
    form_class = BajasForm
    template_name = 'academica/alumnos/alumnos_baja_list.html'

    def get_context_data(self, **kwargs):
        # Llamamos ala implementacion para traer un primer context
        context = super(BajaCreate, self).get_context_data(**kwargs)
        # Agregamos un QuerySet de todos los books
        context['alumnos_list'] = Alumnos.objects.all()
        context['form'] = BajasForm
        return context

    def post(self, request, *args, **kwargs):
        # poniendo inactivo el alumno de baja
        Alumnos.objects.filter(id=request.POST['alumno']).update(is_active=False)
        # agregando el alumno a la tabla alumnoprevio que va a hacer el historico de todos los estudiantes

        a = Alumnos.objects.filter(id=request.POST['alumno']).get()
        historial = AlumnoPrevio(alumno=a)
        historial.save()

        return super(BajaCreate, self).post(request, *args, **kwargs)


class BibliotecaCreate(LoggedInMixin, CreateView):
    model = Biblioteca
    form_class = BibliotecaForm
    template_name = 'academica/deudas/biblioteca_form.html'

    def form_valid(self, form):
        alumnoid = form.cleaned_data['alumno']
        alumnoBaja = Alumnos.objects.get(id=alumnoid.id)
        alumnoBaja.is_deuda = True
        alumnoBaja.save()
        form.save()
        return super(BibliotecaCreate, self).form_valid(form)


class BibliotecaList(LoggedInMixin, ListView):
    model = Biblioteca
    template_name = 'academica/deudas/biblioteca_list.html'

    def get_context_data(self, **kwargs):
        context = super(BibliotecaList, self).get_context_data(**kwargs)
        context['listado'] = Biblioteca.objects.filter(is_active=True)
        return context


class BajaBiblioteca(LoggedInMixin, ListView):
    model = Biblioteca
    template_name = 'academica/deudas/baja_biblioteca.html'

    def get_context_data(self, **kwargs):
        context = super(BajaBiblioteca, self).get_context_data(**kwargs)
        context['form_biblio'] = BibliotecaForm
        context['listado'] = Biblioteca.objects.filter(is_active=True)
        return context


class BibliotecaUpdate(LoggedInMixin, UpdateView):
    model = Biblioteca
    fields = '__all__'
    template_name = 'academica/deudas/biblioteca_form.html'
    form_class = BibliotecaForm


class CentroComputoCreate(LoggedInMixin, CreateView):
    model = CentroComputo
    form_class = CentroComputoForm
    template_name = 'academica/deudas/centrocomputo_form.html'

    def form_valid(self, form):
        alumnoid = form.cleaned_data['alumno']
        alumnoBaja = Alumnos.objects.get(id=alumnoid.id)
        alumnoBaja.is_deuda = True
        alumnoBaja.save()
        form.save()
        return super(CentroComputoCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CentroComputoCreate, self).get_context_data(**kwargs)
        context['form_cc'] = CentroComputoForm

        return context


class CentroComputoList(LoggedInMixin, ListView):
    model = CentroComputo
    template_name = 'academica/deudas/centrocomputo_list.html'

    def get_context_data(self, **kwargs):
        context = super(CentroComputoList, self).get_context_data(**kwargs)
        context['form_cc'] = CentroComputoForm
        context['listado'] = CentroComputo.objects.filter(is_active=True)
        return context


class BajaCC(LoggedInMixin, ListView):
    model = CentroComputo
    template_name = 'academica/deudas/baja_cc.html'

    def get_context_data(self, **kwargs):
        context = super(BajaCC, self).get_context_data(**kwargs)
        context['listado'] = CentroComputo.objects.filter(is_active=True)
        return context


class CCUpdate(LoggedInMixin, UpdateView):
    model = CentroComputo
    fields = '__all__'
    template_name = 'academica/deudas/centrocomputo_form.html'
    form_class = CentroComputoForm


class ContabilidadCreate(LoggedInMixin, CreateView):
    model = Contabilidad
    form_class = ContabilidadForm
    template_name = 'academica/deudas/contabilidad_form.html'

    def form_valid(self, form):
        alumnoid = form.cleaned_data['alumno']
        alumnoBaja = Alumnos.objects.get(id=alumnoid.id)
        alumnoBaja.is_deuda = True
        alumnoBaja.save()
        form.save()
        return super(ContabilidadCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContabilidadCreate, self).get_context_data(**kwargs)
        context['form_conta'] = ContabilidadForm

        return context


class ContabilidadList(LoggedInMixin, ListView):
    model = Contabilidad
    template_name = 'academica/deudas/contabilidad_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContabilidadList, self).get_context_data(**kwargs)
        context['form_conta'] = ContabilidadForm
        context['listado'] = Contabilidad.objects.filter(is_active=True)

        return context


class BajaConta(LoggedInMixin, ListView):
    model = Contabilidad
    template_name = 'academica/deudas/baja_cont.html'

    def get_context_data(self, **kwargs):
        context = super(BajaConta, self).get_context_data(**kwargs)
        context['listado'] = Contabilidad.objects.filter(is_active=True)
        return context


class ContaUpdate(LoggedInMixin, UpdateView):
    model = Contabilidad
    fields = '__all__'
    template_name = 'academica/deudas/contabilidad_form.html'
    form_class = ContabilidadForm


class EncuestaCreate(LoggedInMixin, CreateView):
    model = EncuestaEgresados
    form_class = EncuestaForm
    template_name = 'academica/encuesta/encuesta_form.html'
    success_url = 'encuesta/list'


class EncuestaList(LoggedInMixin, ListView):
    model = EncuestaEgresados
    template_name = 'academica/encuesta/encuesta_list.html'

    def get_context_data(self, **kwargs):
        context = super(EncuestaList, self).get_context_data(**kwargs)
        context['form_encuesta'] = EncuestaForm
        return context


class MunicipioCreate(LoggedInMixin, CreateView):
    model = Municipios
    form_class = MunicipioForm
    template_name = 'academica/localidad/municipio_form.html'
    success_url = 'municipio/list'


class MunicipioList(LoggedInMixin, ListView):
    model = Municipios
    template_name = 'academica/localidad/municipio_list.html'

    def get_context_data(self, **kwargs):
        context = super(MunicipioList, self).get_context_data(**kwargs)
        context['form_municipio'] = MunicipioForm
        return context

    def get_localidad_by_municipio(request):

        if request.is_ajax():
        # alumnosReturn=Alumnos.objects.filter(Q(nom_alumno__contains=request.GET['nombre']) | Q(apellido_paterno__contains=request.GET['apellidoP'])| Q(apellido_materno__contains=request.GET['apellidoM'])|Q(semestre__id__contains=request.GET['semestre'])|Q(no_expediente__contains=request.GET['expediente'])).all()
            print(request.GET['municipio'])

            result=Localidad.objects.filter(municipio=request.GET['municipio']).all()
            retorno = []
            for a in result:
                retorno.append({'id': a.id, 'nombre': a.nombre})

            return HttpResponse(json.dumps(retorno))
        else:
            return redirect('/')


class EstadoCreate(LoggedInMixin, CreateView):
    model = Estados
    form_class = EstadoForm
    template_name = 'academica/localidad/estado_form.html'
    success_url = 'estado/list'


class EstadoList(LoggedInMixin, ListView):
    model = Estados
    template_name = 'academica/localidad/estado_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstadoList, self).get_context_data(**kwargs)
        context['form_estado'] = EstadoForm
        return context


class AulaCreate(LoggedInMixin, CreateView):
    model = Aulas
    form_class = AulaForm
    template_name = 'academica/extracurricular/aula_form.html'
    success_url = 'aula/list'


class AulaList(LoggedInMixin, ListView):
    model = Aulas
    template_name = 'academica/extracurricular/aula_list.html'

    def get_context_data(self, **kwargs):
        context = super(AulaList, self).get_context_data(**kwargs)
        context['form_aula'] = AulaForm
        return context


class Home(LoggedInMixin, TemplateView):
    template_name = 'academica/index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['totalalumnos'] = Alumnos.objects.count()
        context['profesores'] = Maestros.objects.count()
        return context


class ServicioSocialCreate(LoggedInMixin, CreateView):
    model = ServicioHoras
    form_class = ServicioSocialForm
    template_name = 'academica/servicios/servicio_form.html'
    success_url = 'servicio/list'

    def get_context_data(self, **kwargs):
        context = super(ServicioSocialCreate, self).get_context_data(**kwargs)
        context['form_servicio'] = ServicioSocialForm
        return context


class ServicioSocialList(LoggedInMixin, ListView):
    model = ServicioHoras
    template_name = 'academica/servicios/servicio_list.html'

    def get_context_data(self, **kwargs):
        context = super(ServicioSocialList, self).get_context_data(**kwargs)
        context['form_servicio'] = ServicioSocialForm
        context['list_servicio'] = ServicioHoras.objects.filter(is_active=False)
        return context


class ServicioLiberadosList(LoggedInMixin, ListView):
    model = ServicioHoras
    template_name = 'academica/servicios/serviciolib_list.html'

    def get_context_data(self, **kwargs):
        context = super(ServicioLiberadosList, self).get_context_data(**kwargs)
        context['form_servicio'] = ServicioSocialForm
        context['list_liberados'] = ServicioHoras.objects.filter(is_active=True)
        return context


class ServicioUpdate(LoggedInMixin, UpdateView):
    model = ServicioHoras
    fields = '__all__'
    template_name = 'academica/servicios/servicio_update_form.html'
    form_class = ServicioSocialForm


class BecaCreate(LoggedInMixin, CreateView):
    model = Becas
    form_class = BecasForm
    template_name = 'academica/beca/beca_form.html'
    success_url = 'beca/list'


class BecaList(LoggedInMixin, ListView):
    model = Becas
    template_name = 'academica/beca/beca_list.html'

    def get_context_data(self, **kwargs):
        context = super(BecaList, self).get_context_data(**kwargs)
        context['form_beca'] = BecasForm
        return context


class TipoBecaCreate(LoggedInMixin, CreateView):
    model = TipoBeca
    form_class = TiposBecasForm
    template_name = 'academica/beca/tipobeca_form.html'
    success_url = 'tbeca/list'


class TipoBecaList(LoggedInMixin, ListView):
    model = TipoBeca
    template_name = 'academica/beca/tipobeca_list.html'

    def get_context_data(self, **kwargs):
        context = super(TipoBecaList, self).get_context_data(**kwargs)
        context['form_tbeca'] = TiposBecasForm
        return context


class EscuelaCreate(LoggedInMixin, CreateView):
    model = Escuela
    form_class = EscuelaForm
    template_name = 'academica/escuela/escuela_form.html'

    def get_context_data(self, **kwargs):
        context = super(EscuelaCreate, self).get_context_data(**kwargs)
        context['form_escuela'] = EscuelaForm
        return context


class EscuelaList(LoggedInMixin, ListView):
    model = Escuela
    template_name = 'academica/escuela/escuela_list.html'

    def get_context_data(self, **kwargs):
        context = super(EscuelaList, self).get_context_data(**kwargs)
        context['form_escuela'] = EscuelaForm
        return context



class CalificacionesListByMateria(ListView):

    def get_materias_by_profesor(request):

        print(Maestros.objects.get(no_expediente=request.user.no_expediente))
        profesor=Maestros.objects.get(no_expediente=request.user.no_expediente)
        for a in Materias.objects.all():
            print(a.profesor)
        if Materias.objects.filter(profesor=profesor).exists():
            materias = Materias.objects.filter(profesor=profesor)
            return render_to_response('academica/calificacion/profesor_calificaciones.html',
                                      {'listado': materias})
        return render_to_response('academica/calificacion/profesor_calificaciones.html')

    def get_calificaciones_by_materia_ajax(request):
        if request.is_ajax():

            alumnos = Alumnos.objects.all()
            flag = False
            retorno = []
            calificaciones=[]
            # print(Alumnos.objects.get(id=1).plan.materias.all().count())
            idcalificacion=0

            for a in alumnos:#alumnos
                for m in a.plan.materias.all():#recorrro las materias del alumno
                    if m.clave == request.GET['id']:#pregunto si la clave de la materia del estudiante es igual a la materia escogida
                        for c in Calificaciones.objects.all():#recorro las calificaciones para comprobar si ya tiene o no

                            if c.matricula.matricula == a.matricula:#pregunto si en las claificaciones existe el estudiante
                                flag = True
                                idcalificacion=c.id
                                print(c.matricula)
                                break

                        retorno.append({'nombre': a.nom_alumno, 'apellido_paterno': a.apellido_paterno,
                                        'apellido_materno': a.apellido_materno, 'matricula': a.matricula, 'id': a.id,
                                        'flag': flag,'calificacion_id':idcalificacion})

            return HttpResponse(json.dumps(retorno))
        else:
            redirect('academica/calificacion/profesor_calificaciones.html')

