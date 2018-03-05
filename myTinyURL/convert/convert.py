from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import URL
import random, string

class Convert:
    CONST_LENGTH = 6
    def long2short(httpurl):
        short_id = Convert.gen()
        record = URL(httpurl=httpurl, short_id=short_id)
        record.save()
        response = settings.SITE_URL + "/" + short_id
        return response

    def short2long(short_id):
        url = get_object_or_404(URL, pk=short_id)
        url.count += 1
        url.save()
        return url.httpurl

    def gen():
        dic = string.ascii_uppercase + string.digits + string.ascii_lowercase
        short_id = ''
        while True:
            for i in range(Convert.CONST_LENGTH):
                short_id += random.choice(dic)
            try:
                tmp = URL.objects.get(pk=short_id)
            except:
                return short_id
