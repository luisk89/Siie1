from django.shortcuts import _get_queryset
from academica.models import PlanEstudio,Extracurriculares, Alumnos, Empresas, Semestre, Municipios

__author__ = 'Luisk'

def getPlanListado():
    return PlanEstudio.objects.filter(is_active=True)


def getCicloSemestral():
    return Semestre.objects.all()

def getEmpresas():
    return Empresas.objects.all()


def getSemestreActive():
    result= Semestre.objects.filter(vigente=True)
    return result

def getEstudiantesPuedenSS():
    result= []
    for a in Alumnos.objects.all():
        cont=0
        if (a.extracurriculares.count()>=2):
            for b in a.extracurriculares.all():
                if(b.is_active):
                    cont+=1
            if cont >=2:
                result.append(Alumnos)

    Alumnos.objects.filter()
    return result

def getAlumnos():
    return Alumnos.objects.all()

def getMunicipios():
    return Municipios.objects.all()