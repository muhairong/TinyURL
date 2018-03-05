from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # /convert/short_id/
    path('<slug:short_id>/', views.redirect, name='redirect'),
    # /convert/shorten/
    path('shorten', views.shorten, name='shorten'),
]
