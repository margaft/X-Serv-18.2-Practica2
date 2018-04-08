from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from acorta.models import Urls
from django.views.decorators.csrf import csrf_exempt

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
         
        texto += "<form action='' method='POST'>"
        texto += "URL a acortar <input type='text' name='urlFormulario'>"
        texto += "<input type='submit' value='Acortar'></form>"

    elif request.method == 'POST':
        urlFormulario = request.POST['urlFormulario']
        if urlFormulario == "":
            texto = "<p><h4>¡No has introducido ninguna URL!<h4></p>"
            texto += "<a href='http://localhost:8000'>Si desea volver a la aplicación 'Acortador de URLs' pulse sobre este enlace</a>"
            return HttpResponseBadRequest(texto)
        elif not urlFormulario.startswith("http://") and not urlFormulario.startswith("https://"):
            urlFormulario = "http://" + urlFormulario
        try:
            URLNueva = Urls.objects.get(urlFormulario = urlFormulario)
            texto = "Esa URL ya ha sido añadida con anterioridad"
            texto += "<p>URL acortada: <a href='" + URLNueva.urlFormulario + "'>" + str(URLNueva.id) + "</a>"
            texto += " --> " + "<a href='" + URLNueva.urlFormulario + "'>" + URLNueva.urlFormulario + "</a></p>"
            texto += "<a href=''>Si desea volver a la aplicación 'Acortador de URLs' pulse sobre este enlace</a>"
            return HttpResponse(texto)
            
        except Urls.DoesNotExist:
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
        
    except Urls.DoesNotExist:
        texto = "<p>La URL que has introducido no está disponible</p>"
        texto += "<a href='http://localhost:8000'>Si desea volver a la aplicación 'Acortador de URLs' pulse sobre este enlace</a>"
        return HttpResponse(texto)
        
def Error(request):
	return HttpResponse('<h1>ERROR<h1>')
