from django.contrib import admin
from convert.models import URL,LatestId
# Register your models here.

class UrlsAdmin(admin.ModelAdmin):
    """ Register Url model
        Ordered by the pub_date field
    """
    list_display = ('short_id', 'http_url', 'pub_date', 'count')
    ordering = ['pub_date']

class LatestIdAdmin(admin.ModelAdmin):
    """ Register Url model
    """
    list_display = ('id', 'short_id',)


# Add these two models on admin page
admin.site.register(URL, UrlsAdmin)
admin.site.register(LatestId, LatestIdAdmin)
