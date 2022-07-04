from xml.etree.ElementInclude import include
from django.urls import path
from admin import views

urlpatterns = [
    path('statistics', views.get_statistics_util),
    path('statistics/<str:mobile>', views.get_statistics),
    path('add_authority', views.add_authority),
    path('manage_category', views.manage_category_util),
    path('manage_category/<str:mobile>', views.manage_category)
]