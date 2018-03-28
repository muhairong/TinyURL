from django.db import models


class URL(models.Model):
    """ URL model
    A record has four fields:
    the short_id (is the primary key),
    the corresponding long url http_url,
    the publication date pub_date,
    and the click count
    """
    short_id = models.SlugField(max_length=6, primary_key=True)
    http_url = models.URLField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.short_id


#
class LatestId(models.Model):
    id = models.IntegerField(primary_key=True)
    short_id = models.SlugField(max_length=6)
