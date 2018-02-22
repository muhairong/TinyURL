from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import URL
from django.conf import settings
import random, string

# Create your views here.

def index(request):
    return HttpResponse("Hello, welcome to my shorturl convert page.")

def shorten(request, url):
    if (url == ''):
        return HttpResponse("Error...Empty url")
    print 
    short_id = gen()
    record = URL(httpurl=url, short_id=short_id)
    record.save()
    response = settings.SITE_URL + "/" + short_id
    return HttpResponse(response)


def redirect(request, short_id):
    url = get_object_or_404(URL, pk=short_id)
    url.count += 1
    url.save()
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
