from django.contrib import admin
from convert.models import URL
# Register your models here.

class UrlsAdmin(admin.ModelAdmin):
    list_display = ('short_id','httpurl','pub_date', 'count')

admin.site.register(URL, UrlsAdmin)
