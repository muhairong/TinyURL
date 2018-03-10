from django.contrib import admin
from convert.models import URL
# Register your models here.

class UrlsAdmin(admin.ModelAdmin):
    """ Register Url model
        Ordered by the pub_date field
    """
    list_display = ('short_id', 'http_url', 'pub_date', 'count')
    ordering = ['pub_date']

admin.site.register(URL, UrlsAdmin)
