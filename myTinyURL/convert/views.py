from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
import logging
from .convert import Convert

logging.getLogger().setLevel(logging.INFO)

def index(request):
    return render(request, 'convert/index.html')

def shorten(request):
    url = request.POST['url']
    logging.info('received url %s', url)
    if (url == ''):
        logging.error('received url is empty')
        return JsonResponse("Error: blank url...", safe=False)
    response = Convert.long2short(url)
    logging.info('return response is %s', response)
    return JsonResponse(response, safe=False)

def redirect(request, short_id):
    url = Convert.short2long(short_id)
    logging.info('long url is %s',url)
    rawurl = "https://" + url
    return HttpResponseRedirect(rawurl)