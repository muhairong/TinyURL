import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse

from .convert import Convert

logging.getLogger().setLevel(logging.INFO)

def index(request):
    """ Display the index page.

    :return: /convert/index.html
    """
    return render(request, 'convert/index.html')

def shorten(request):
    """ According to the post url, generate short url.

    Get post url. Call Convert.long2short to get the short url.

    :return: The short url just generated at the index page
    """
    url = request.POST['url']
    #print(type(url))
    logging.info('received url %s', url)
    if (url is ''):
        logging.error('received url is empty')
        return JsonResponse("Error: blank url...", safe=False)
    response = Convert.long2short(url)
    logging.info('return response is %s', response)
    return JsonResponse(response, safe=False)

def redirect(request, short_id):
    """ According to the short_id, get the corresponding long url.

    Call Convert.short2long to get the long url.
    Redirect to this url.

    :return: The corresponding long url page
    """
    url = Convert.short2long(short_id)
    logging.info('long url is %s', url)
    raw_url = "https://" + url
    return JsonResponse(raw_url, safe=False)
    # Too slow
    # return HttpResponseRedirect(raw_url)