from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from .models import URL
from django.conf import settings
import random, string
import logging

logging.getLogger().setLevel(logging.INFO)
# Create your views here.

def index(request):
    return render(request, 'convert/index.html')

def shorten(request):
    url = request.POST['url']
    logging.info('received url %s', url)
    #print("received short url request:{}".format(url))
    if (url == ''):
        logging.error('received url is empty')
        #print("received url is empty")
        return JsonResponse("Error: blank url...", safe=False)
    short_id = gen()
    record = URL(httpurl=url, short_id=short_id)
    record.save()
    response = settings.SITE_URL + "/" + short_id
    #print("return response: {}".format(response))
    logging.info('return response is %s', response)
    return JsonResponse(response, safe=False)

def redirect(request, short_id):
    url = get_object_or_404(URL, pk=short_id)
    url.count += 1
    url.save()
    #print(url.httpurl)
    logging.info('long url is %s',url.httpurl)
    return HttpResponse(url.httpurl)

def gen():
    length = 6
    dic = string.ascii_uppercase + string.digits + string.ascii_lowercase
    short_id = ''
    while True:
        for i in range(length):
            short_id += random.choice(dic)
        try:
            tmp = URL.objects.get(pk=short_id)
        except:
            return short_id
