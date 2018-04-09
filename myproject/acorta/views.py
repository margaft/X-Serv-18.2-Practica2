#Margarita Fernández Torrejón

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from acorta.models import Urls
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@csrf_exempt
def acortar(request):
	ListaURLs = Urls.objects.all();
	if request.method == 'GET':
		if Urls.objects.all().exists():
			texto = "<h3>Acortador de URLs</h3>"
			for URL in ListaURLs:
				texto += "<li>/" + str(URL.id) + " ---- " + URL.urlFormulario
		else:	
			texto = "<h3>Todavía no se ha acortado ninguna URL</h3></br>"
		 
		texto += "<form action='' method='POST'>"+"URL a acortar <input type='text' name='urlFormulario'>"+"<input type='submit' value='Acortar'></form>"

	elif request.method == 'POST':
		try:
			urlFormulario = request.POST['urlFormulario']
		except KeyError:
			texto = "Error"
			return HttpResponseBadRequest(texto)
		#En el cuerpo del POST no hay URL
		if urlFormulario == "":
			texto = "<p><h4>¡No has introducido ninguna URL!<h4></p>"
			texto += "<a href='http://localhost:8000'>Si desea volver a la aplicación 'Acortador de URLs' pulse sobre este enlace</a>"
			return HttpResponseBadRequest(texto)
		#La URL introducida empieza por HTTP o HTTPS entonces la url se queda igua
		elif urlFormulario.startswith("http://") and not urlFormulario.startswith("https://"):
			urlFormulario = urlFormulario
		#La URL introducida no empieza por HTTP entonces se lo añado
		else:
			urlFormulario = "http://" + urlFormulario
		try:
			#La URL ya está en la BD
			URLNueva = Urls.objects.get(urlFormulario = urlFormulario)
			texto = "Esa URL ya ha sido añadida con anterioridad"
			texto += "<p>URL acortada: <a href='" + URLNueva.urlFormulario + "'>" + str(URLNueva.id) + "</a>" + " ---- " + "<a href='" + URLNueva.urlFormulario + "'>" + URLNueva.urlFormulario + "</a></p>"
			texto += "<a href=''>Si desea volver a la aplicación 'Acortador de URLs' pulse sobre este enlace</a>"
			return HttpResponse(texto)
			
		except Urls.DoesNotExist: #La URL no está en la BD
			URLNueva = Urls(urlFormulario = urlFormulario)
			URLNueva.save()
		texto = ("<p>URL acortada: <a href='" + URLNueva.urlFormulario + "'>" + str(URLNueva.id) + "</a>" +
					 " ---- " + "<a href='" + URLNueva.urlFormulario + "'>" + URLNueva.urlFormulario + "</a></p>")
		texto += "<a href=''>Si desea volver a la aplicación 'Acortador de URLs' pulse sobre este enlace</a>"
		
	return HttpResponse(texto)

def redireccion(request, URL_acortada):
	try:
		urlFormulario = Urls.objects.get(id = URL_acortada).urlFormulario
		return HttpResponseRedirect(urlFormulario)
		
	except ObjectDoesNotExist:
		texto = "<p>La URL que has introducido no está disponible</p>"
		texto += "<a href='http://localhost:8000'>Si desea volver a la aplicación 'Acortador de URLs' pulse sobre este enlace</a>"
		return HttpResponse(texto)
		
def Error(request):
	return HttpResponse('<h1>ERROR<h1>')
