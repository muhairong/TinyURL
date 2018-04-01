import time, logging
# import random, string

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
from django.db import transaction

from .models import URL, LatestId

logging.getLogger().setLevel(logging.INFO)


class Convert():
    """core engine of url conversion
    """
    SHORT_ID_LENGTH = 6
    WRITE_SYN = 1

    @classmethod
    def long2short(cls, http_url):
        """Convert the given long url to a shorter one.

        Work as following steps:
        Get the latest short_id from LatestId table, then add 1 to generate a new short_id
        Update latest and save the new recode in URL table
        Generate the response using SITE_URL.

        Args:
            http_url: a url we want to convert
            type: str

        Return:
            The response(SITE_URL + short_id) we just create
            type: str
        """
        with transaction.atomic():
            latest = LatestId.objects.select_for_update().get(id=1)
            latest_short_id = latest.short_id
            short_id = str(int(latest_short_id) + 1).rjust(Convert.SHORT_ID_LENGTH, '0')
            logging.info('new short_id is %s', short_id)
            latest.short_id = short_id
            # logging.info('latest short_id is %s', latest.short_id)
            # time.sleep(4)
            # logging.info('done sleep')
            latest.save()
            record = URL(http_url=http_url, short_id=short_id)
            record.save()

        response = settings.SITE_URL + '/' + short_id
        return response

    @classmethod
    def short2long(cls, short_id):
        """Convert given short_id to its corresponding long url.

        According to Convert.WRITE_SYN, call short2long_SYN or short2long_NOT_SYN to find httpurl

        Args:
            short_id: a short url we want to convert
            type: str

        Return:
            The corresponding long url
            type: str
        """
        if Convert.WRITE_SYN:
            return Convert.short2long_SYN(short_id)
        else:
            # Read operation has no need to update and lock the row in database
            return Convert.short2long_NOT_SYN(short_id)

    @classmethod
    def short2long_SYN(cls, short_id):
        """Convert given short_id to its corresponding long url synchronously

        Find in the database, the primary key is short_id.
        Lock the corresponding row in database. If found, update this record click counts and save it.

        :param
            short_id: a short url we want to convert
            type: str
        :return:
            The corresponding long url
            type: str
        """
        with transaction.atomic():
            try:
                url = URL.objects.select_for_update().get(short_id=short_id)
            except URL.DoesNotExist:
                raise Http404("Short_id does not exist")
            # url = get_object_or_404(URL, pk=short_id)
            url.count += 1
            url.save()
        return url.http_url

    @classmethod
    def short2long_NOT_SYN(cls, short_id):
        """Convert given short_id to its corresponding long url

        Simply find in database and return the corresponding long url.

        :param
            short_id: a short url we want to convert
            type: str
        :return:
            The corresponding long url
            type: str
        """
        url = get_object_or_404(URL, pk=short_id)
        return url.http_url

    @classmethod
    def gen_short_id(cls):
        """generate a random short_id.

        Generate a short_id randomly.
        Check if the short_id exists in the database. Return if it does. Otherwise, generate a new one.

        Return:
            A unique short_id
            type: str

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
        """
