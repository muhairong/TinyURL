from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import URL
import random, string

class Convert():
    """core engine of url conversion
    """

    SHORT_ID_LENGTH = 6

    @classmethod
    def long2short(cls, http_url):
        """Convert the given long url to a shorter one.

        Work as following steps:
        Call gen_shortid() to generate a random short id.
        Save to database.
        Generate the response using SITE_URL.

        Args:
            http_url: a url we want to convert
            type: str

        Return:
            The response(SITE_URL + short_id) we just create
            type: str
        """
        short_id = Convert.gen_short_id()
        record = URL(http_url=http_url, short_id=short_id)
        record.save()
        response = settings.SITE_URL + '/' + short_id
        return response

    @classmethod
    def short2long(cls, short_id):
        """Convert given short_id to its corresponding long url.

        Find in the database, the primary key is short_id.
        If found, update this record click counts and save it.

        Args:
            short_id: a short url we want to convert
            type: str

        Return:
            The corresponding long url
            type: str
        """
        url = get_object_or_404(URL, pk=short_id)
        url.count += 1
        url.save()
        return url.http_url

    @classmethod
    def gen_short_id(cls):
        """generate a random short_id.

        Generate a short_id randomly.
        Check if the short_id exists in the database. Return if it does. Otherwise, generate a new one.

        Return:
            A unique short_id
            type: str
        """
        char_candidates = string.ascii_uppercase + string.digits + string.ascii_lowercase
        while True:
            short_id = ''.join(
                random.choice(char_candidates)
                for i in range(Convert.SHORT_ID_LENGTH)
            )
            try:
                tmp = URL.objects.get(pk=short_id)
            except:
                return short_id
