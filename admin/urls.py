from xml.etree.ElementInclude import include
from django.urls import path
from admin import views

urlpatterns = [
    path('statistics', views.get_statistics),
    path('statistics/<str:mobile>', views.get_statistics_util),
    path('add_authority', views.add_authority),
    path('edit_authority', views.edit_authority),
    path('edit_authority/<str:mobile>', views.edit_authority_util),
    path('manage_category', views.manage_category),
    path('manage_category/<str:mobile>', views.manage_category_util)
]