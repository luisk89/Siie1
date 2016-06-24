from dajax.core import Dajax
from dajaxice.core import dajaxice_functions
from academica.models import PlanEstudio

__author__ = 'Luisk'
#
# def getMunicipiosByProvincia(request,id_provincia):
# 	dajax = Dajax()
# 	objects = Municipio.objects.filter(provincia=id_provincia)
# 	options = '<option selected="selected" value="">---------</option>'
# 	for obj in objects:
# 		options += '<option value="%s">%s</option>' % (obj.id_mcpio,obj.nombre)
# 	dajax.assign('#id_municipio','innerHTML', options)
# 	return dajax.json()
#
# dajaxice_functions.register(getMunicipiosByProvincia)

def getPlandeEstudios(request):
	dajax = Dajax()
	options = '<option selected="selected" value="">---------</option>'
	plan = PlanEstudio.objects.all()
	for p in plan:
		options += '<optgroup label="%s">' % p.nom_plan
		options += '<option value="%s">%s</option>'% (p.id,p.get_full_name())
		options += '</optgroup>'
	#~ dajax.assign('#id_participantes','innerHTML',options)
	return dajax.json()
dajaxice_functions.register(getPlandeEstudios)
