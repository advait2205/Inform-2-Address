from xml.etree.ElementInclude import include
from django.urls import path
from admin import views

urlpatterns = [
    path('statistics', views.get_statistics)
]